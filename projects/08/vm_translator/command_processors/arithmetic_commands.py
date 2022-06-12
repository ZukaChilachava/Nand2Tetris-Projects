from dataclasses import dataclass

from n2t.core.vm_translator.commands import DynamicCommands, StaticCommands


@dataclass
class AddSubCommand:
    @staticmethod
    def get_command(operation: str) -> str:
        return (
            f"{StaticCommands.get_last_two()}\n"
            f"{operation}\n"
            f"{StaticCommands.increment_stack()}"
        )


@dataclass
class AddCommand:
    def get_command(self) -> str:
        return AddSubCommand.get_command("M=D+M")


@dataclass
class SubCommand:
    def get_command(self) -> str:
        return AddSubCommand.get_command("M=M-D")


@dataclass
class NegationCommand:
    def get_command(self) -> str:
        return (
            f"{StaticCommands.decrement_stack()}\n"
            f"{StaticCommands.dereference_sp()}\n"
            f"M=-M\n"
            f"{StaticCommands.increment_stack()}"
        )


class ComparisonXY:
    @staticmethod
    def get_command(jump: str, label_name: str) -> str:
        return (
            f"{StaticCommands.get_last_two()}\n"
            f"D=D-M\n"
            f"M=0\n"
            f"{DynamicCommands.get_label(label_name)}\n"
            f"D;{jump}\n"
            f"@SP\n"
            f"A=M\n"
            f"M=-1\n"
            f"({label_name})\n"
            f"{StaticCommands.increment_stack()}"
        )


class CompCommand:
    jump_operation: str
    label: str
    count: int

    def get_command(self) -> str:
        result: str = ComparisonXY.get_command(
            self.jump_operation, f"{self.label}{self.count}"
        )
        self.count += 1
        return result


class GreaterThanCommand(CompCommand):
    jump_operation: str = "JGE"
    label: str = "GT"
    count: int = 0


class LessThanCommand(CompCommand):
    jump_operation: str = "JLE"
    label: str = "LT"
    count: int = 0


class EqualityCommand(CompCommand):
    jump_operation: str = "JNE"
    label: str = "EQ"
    count: int = 0


class LogicalOnXY:
    operation: str

    def get_command(self) -> str:
        return (
            f"{StaticCommands.get_last_two()}\n"
            f"M=D{self.operation}M\n"
            f"{StaticCommands.increment_stack()}"
        )


class AndOperation(LogicalOnXY):
    operation: str = "&"


class OrOperation(LogicalOnXY):
    operation: str = "|"


class NotCommand:
    def get_command(self) -> str:
        return (
            f"{StaticCommands.decrement_stack()}\n"
            f"{StaticCommands.dereference_sp()}\n"
            f"M=!M\n"
            f"{StaticCommands.increment_stack()}"
        )
