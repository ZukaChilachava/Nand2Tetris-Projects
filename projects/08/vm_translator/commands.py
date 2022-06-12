class StaticCommands:
    @staticmethod
    def increment_stack() -> str:
        return "@SP\nM=M+1"

    @staticmethod
    def decrement_stack() -> str:
        return "@SP\nM=M-1"

    @staticmethod
    def dereference_sp() -> str:
        return "A=M"

    @staticmethod
    def set_stack() -> str:
        return f"@SP\n{StaticCommands.dereference_sp()}\nM=D"

    @staticmethod
    def push_to_stack() -> str:
        return f"{StaticCommands.set_stack()}\n{StaticCommands.increment_stack()}"

    @staticmethod
    def memorise_stack_value() -> str:
        return f"{StaticCommands.dereference_sp()}\nD=M"

    @staticmethod
    def get_last_two() -> str:
        return (
            f"{StaticCommands.decrement_stack()}\n"
            f"{StaticCommands.memorise_stack_value()}\n"
            f"{StaticCommands.decrement_stack()}\n"
            f"{StaticCommands.dereference_sp()}"
        )

    @staticmethod
    def set_bootstrap_stack() -> str:
        return "@256\nD=A\n@SP\nM=D"

    @staticmethod
    def unconditional_jump() -> str:
        return "0;JMP"


class DynamicCommands:
    GENERAL_PURPOSE_REGISTER = "R13"

    @staticmethod
    def set_constant(const: str) -> str:
        return f"@{const}\nD=A"

    @staticmethod
    def get_label(label_name: str) -> str:
        return f"@{label_name}"

    @staticmethod
    def memorise_index(i: str) -> str:
        return f"@{i}\nD=A"

    @staticmethod
    def go_to_ith(ram_label: str, i: str) -> str:
        return f"{DynamicCommands.memorise_index(i)}\n@{ram_label}\nA=D+M"

    @staticmethod
    def get_static_variable(file_name: str, i: str) -> str:
        return f"@{file_name}.{i}"

    @staticmethod
    def set_general_value() -> str:
        return f"@{DynamicCommands.GENERAL_PURPOSE_REGISTER}\nM=D"

    @staticmethod
    def get_function_label(label: str, function_name: str) -> str:
        return f"{function_name}${label}"

    @staticmethod
    def get_return_label(function_name: str, count: str) -> str:
        return f"{function_name}$ret.{count}"
