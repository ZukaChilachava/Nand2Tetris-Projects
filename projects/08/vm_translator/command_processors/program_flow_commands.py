from dataclasses import dataclass

from n2t.core.vm_translator.commands import DynamicCommands, StaticCommands


@dataclass
class LabelCommand:
    function_name: str
    label: str

    def get_command(self) -> str:
        return f"({DynamicCommands.get_function_label(self.function_name, self.label)})"


@dataclass
class ConditionalGoToCommand:
    function_name: str
    label: str

    def get_command(self) -> str:

        return (
            f"{StaticCommands.decrement_stack()}\n"
            f"{StaticCommands.memorise_stack_value()}\n"
            f"@{DynamicCommands.get_function_label(self.function_name, self.label)}\n"
            f"D;JNE"
        )


@dataclass
class UnconditionalGoToCommand:
    function_name: str
    label: str

    def get_command(self) -> str:
        return (
            f"@{DynamicCommands.get_function_label(self.function_name, self.label)}\n"
            f"{StaticCommands.unconditional_jump()}"
        )
