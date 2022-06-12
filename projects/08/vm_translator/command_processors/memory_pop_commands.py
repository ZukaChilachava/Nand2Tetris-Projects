from dataclasses import dataclass

from n2t.core.vm_translator.command_protocols import ArgCommand
from n2t.core.vm_translator.commands import DynamicCommands, StaticCommands


class GenericPopCommand:
    assembly_arg: str

    def get_command(self, arg: str) -> str:
        return (
            f"{DynamicCommands.memorise_index(i=arg)}\n"
            f"@{self.assembly_arg}\n"
            f"D=D+M\n"
            f"{DynamicCommands.set_general_value()}\n"
            f"{StaticCommands.decrement_stack()}\n"
            f"{StaticCommands.memorise_stack_value()}\n"
            f"@{DynamicCommands.GENERAL_PURPOSE_REGISTER}\n"
            f"A=M\n"
            f"M=D"
        )


class LocalPopCommand(GenericPopCommand):
    assembly_arg: str = "LCL"


class ArgumentPopCommand(GenericPopCommand):
    assembly_arg: str = "ARG"


class ThisPopCommand(GenericPopCommand):
    assembly_arg: str = "THIS"


class ThatPopCommand(GenericPopCommand):
    assembly_arg: str = "THAT"


@dataclass
class StaticPopCommand:
    file_name: str

    def get_command(self, arg: str) -> str:
        return (
            f"{StaticCommands.decrement_stack()}\n"
            f"{StaticCommands.memorise_stack_value()}\n"
            f"{DynamicCommands.get_static_variable(self.file_name, arg)}\n"
            f"M=D"
        )


class TempPopCommand:
    TEMP_START: int = 5

    def get_command(self, arg: str) -> str:
        return (
            f"{StaticCommands.decrement_stack()}\n"
            f"{StaticCommands.memorise_stack_value()}\n"
            f"@{self.TEMP_START + int(arg)}\n"
            f"M=D"
        )


class PointerPopCommand:
    MAP = {"0": "THIS", "1": "THAT"}

    def get_command(self, arg: str) -> str:
        return (
            f"{StaticCommands.decrement_stack()}\n"
            f"{StaticCommands.memorise_stack_value()}\n"
            f"@{self.MAP[arg]}\n"
            f"M=D"
        )


class NoCommand:
    def get_command(self, arg: str) -> str:
        return ""


class PopCommand:
    arg1: str
    arg2: str

    MAP: dict[str, ArgCommand] = {
        "local": LocalPopCommand(),
        "argument": ArgumentPopCommand(),
        "this": ThisPopCommand(),
        "that": ThatPopCommand(),
        "pointer": PointerPopCommand(),
        "temp": TempPopCommand(),
    }

    def __init__(self, arg1: str, arg2: str, file_name: str) -> None:
        self.arg1 = arg1
        self.arg2 = arg2
        self.MAP["static"] = StaticPopCommand(file_name)

    def get_command(self) -> str:
        command: ArgCommand = self.MAP.get(self.arg1, NoCommand())
        result: str = command.get_command(self.arg2)
        return result
