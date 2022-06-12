from n2t.core.vm_translator.command_processors.arithmetic_commands import (
    AddCommand,
    AndOperation,
    EqualityCommand,
    GreaterThanCommand,
    LessThanCommand,
    NegationCommand,
    NotCommand,
    OrOperation,
    SubCommand,
)
from n2t.core.vm_translator.command_processors.memory_pop_commands import PopCommand
from n2t.core.vm_translator.command_processors.memory_push_commands import PushCommand
from n2t.core.vm_translator.command_protocols import VMCommand


class CommandChecker:
    PUSH_C: str = "push"
    POP_C: str = "pop"

    ARITHMETIC_MAP: dict[str, VMCommand] = {
        "add": AddCommand(),
        "sub": SubCommand(),
        "neg": NegationCommand(),
        "eq": EqualityCommand(),
        "gt": GreaterThanCommand(),
        "lt": LessThanCommand(),
        "and": AndOperation(),
        "or": OrOperation(),
        "not": NotCommand(),
    }

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name

    def get_command_type(self, line: str) -> VMCommand:
        arg_list: list[str] = line.split(" ")
        command: VMCommand
        if len(arg_list) > 1:
            if arg_list[0] == self.PUSH_C:
                command = PushCommand(
                    arg1=arg_list[1], arg2=arg_list[2], file_name=self.file_name
                )
            elif arg_list[0] == self.POP_C:
                command = PopCommand(
                    arg1=arg_list[1], arg2=arg_list[2], file_name=self.file_name
                )
        else:
            command = self.ARITHMETIC_MAP[arg_list[0]]

        return command
