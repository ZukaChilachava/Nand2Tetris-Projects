from dataclasses import dataclass

from n2t.core.vm_translator.command_processors.memory_pop_commands import (
    ArgumentPopCommand,
)
from n2t.core.vm_translator.command_processors.memory_push_commands import ConstCommand
from n2t.core.vm_translator.commands import DynamicCommands, StaticCommands


class CallCommand:

    SAVE_LABELS: list[str] = ["LCL", "ARG", "THIS", "THAT"]

    def __init__(
        self, function_name: str, arg_number: str, index: int, current_function: str
    ) -> None:
        self.current_function = current_function
        self.function_name = function_name
        self.arg_number = arg_number
        self.index = str(index)

    def get_command(self) -> str:
        return_label: str = DynamicCommands.get_return_label(
            function_name=self.current_function, count=self.index
        )
        push_return_label: str = (
            f"{DynamicCommands.memorise_index(return_label)}\n"
            f"{StaticCommands.push_to_stack()}\n"
        )

        save_commands: str = ""
        for label in self.SAVE_LABELS:
            save_commands += (
                f"{DynamicCommands.get_label(label)}\n"
                f"D=M\n"
                f"{StaticCommands.push_to_stack()}\n"
            )

        reposition_arg: str = (
            f"{DynamicCommands.memorise_index('5')}\n"
            f"{DynamicCommands.get_label(self.arg_number)}\n"
            f"D=D+A\n"
            f"@SP\n"
            f"D=M-D\n"
            f"{DynamicCommands.get_label('ARG')}\n"
            f"M=D\n"
        )

        reposition_lcl: str = "@SP\nD=M\n@LCL\nM=D\n"
        goto_function: str = (
            f"{DynamicCommands.get_label(self.function_name)}\n"
            f"{StaticCommands.unconditional_jump()}\n"
        )

        set_return_location: str = f"({return_label})"

        return (
            push_return_label
            + save_commands
            + reposition_arg
            + reposition_lcl
            + goto_function
            + set_return_location
        )


@dataclass
class FunctionCommand:
    function_name: str
    local_number: str
    PUSH_VALUE: str = "0"

    def get_command(self) -> str:
        result: str = f"({self.function_name})"
        for _ in range(int(self.local_number)):
            result += "\n" + ConstCommand().get_command(self.PUSH_VALUE)

        return result


class ReturnCommand:
    PIVOT_ADDRESS: str = "@LCL"
    RESTORE_OFFSET_MAP: dict[str, str] = {
        "LCL": "1",
        "ARG": "2",
        "THIS": "3",
        "THAT": "4",
    }

    def get_command(self) -> str:
        save_return_address: str = (
            f"{self.PIVOT_ADDRESS}\nD=M\n@5\nD=D-A\n@R14\nM=D\nA=M\nD=M\n@R15\nM=D\n"
        )

        pop_return_value: str = ArgumentPopCommand().get_command("0") + "\n"
        reposition_stack_pointer: str = "@ARG\nD=M+1\n@SP\nM=D\n"

        restore_state: str = ""
        for label, offset in self.RESTORE_OFFSET_MAP.items():
            restore_state += (
                f"@{offset}\n"
                f"D=A\n"
                f"@R14\n"
                f"A=D+M\n"
                f"D=M\n"
                f"@{label}\n"
                f"M=D\n"
            )

        jump_to_next_instruction: str = (
            f"@R15\nA=M\n{StaticCommands.unconditional_jump()}"
        )

        return (
            save_return_address
            + pop_return_value
            + reposition_stack_pointer
            + restore_state
            + jump_to_next_instruction
        )
