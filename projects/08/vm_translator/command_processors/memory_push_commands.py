from dataclasses import dataclass

from n2t.core.vm_translator.command_processors.memory_pop_commands import NoCommand
from n2t.core.vm_translator.command_protocols import ArgCommand
from n2t.core.vm_translator.commands import DynamicCommands, StaticCommands


class GenericPushCommand:
    assembly_arg: str

    def get_command(self, arg: str) -> str:
        return (
            f"{DynamicCommands.go_to_ith(self.assembly_arg, arg)}\n"
            f"D=M\n"
            f"{StaticCommands.push_to_stack()}"
        )


class LocalPushCommand(GenericPushCommand):
    assembly_arg: str = "LCL"


class ArgumentPushCommand(GenericPushCommand):
    assembly_arg: str = "ARG"


class ThisPushCommand(GenericPushCommand):
    assembly_arg: str = "THIS"


class ThatPushCommand(GenericPushCommand):
    assembly_arg: str = "THAT"


class TempPushCommand:
    TEMP_START: int = 5

    def get_command(self, arg: str) -> str:
        return f"@{self.TEMP_START + int(arg)}\nD=M\n{StaticCommands.push_to_stack()}"


class ConstCommand:
    def get_command(self, arg: str) -> str:
        return (
            f"{DynamicCommands.set_constant(const=arg)}\n"
            f"{StaticCommands.push_to_stack()}"
        )


@dataclass
class StaticPushCommand:
    file_name: str

    def get_command(self, arg: str) -> str:
        return (
            f"{DynamicCommands.get_static_variable(file_name=self.file_name, i=arg)}\n"
            f"D=M\n"
            f"{StaticCommands.push_to_stack()}"
        )


class PointerPushCommand:
    MAP = {"0": "THIS", "1": "THAT"}

    def get_command(self, arg: str) -> str:
        return f"@{self.MAP[arg]}\nD=M\n{StaticCommands.push_to_stack()}"


class PushCommand:
    arg1: str
    arg2: str

    MAP: dict[str, ArgCommand] = {
        "constant": ConstCommand(),
        "local": LocalPushCommand(),
        "argument": ArgumentPushCommand(),
        "this": ThisPushCommand(),
        "that": ThatPushCommand(),
        "temp": TempPushCommand(),
        "pointer": PointerPushCommand(),
    }

    def __init__(self, arg1: str, arg2: str, file_name: str) -> None:
        self.arg1 = arg1
        self.arg2 = arg2
        self.MAP["static"] = StaticPushCommand(file_name)

    def get_command(self) -> str:
        command: ArgCommand = self.MAP.get(self.arg1, NoCommand())
        result: str = command.get_command(self.arg2)
        return result
