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
from n2t.core.vm_translator.command_processors.function_commands import (
    CallCommand,
    FunctionCommand,
    ReturnCommand,
)
from n2t.core.vm_translator.command_processors.memory_pop_commands import PopCommand
from n2t.core.vm_translator.command_processors.memory_push_commands import PushCommand
from n2t.core.vm_translator.command_processors.program_flow_commands import (
    ConditionalGoToCommand,
    LabelCommand,
    UnconditionalGoToCommand,
)
from n2t.core.vm_translator.command_protocols import VMCommand


class CommandChecker:
    CALL: str = "call"
    POP_C: str = "pop"
    LABEL: str = "label"
    PUSH_C: str = "push"
    FUNCTION: str = "function"
    UNCONDITIONAL_GOTO: str = "goto"
    CONDITIONAL_GOTO: str = "if-goto"

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
        "return": ReturnCommand(),
    }

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.current_function = ""
        self.call_count = 0

    def get_command_type(self, line: str) -> VMCommand:
        arg_list: list[str] = list(filter(None, line.split(" ")))
        command: VMCommand
        if len(arg_list) > 1:
            match arg_list[0]:
                case self.PUSH_C:
                    command = PushCommand(
                        arg1=arg_list[1], arg2=arg_list[2], file_name=self.file_name
                    )
                case self.POP_C:
                    command = PopCommand(
                        arg1=arg_list[1], arg2=arg_list[2], file_name=self.file_name
                    )
                case self.LABEL:
                    command = LabelCommand(
                        function_name=self.current_function, label=arg_list[1]
                    )
                case self.UNCONDITIONAL_GOTO:
                    command = UnconditionalGoToCommand(
                        function_name=self.current_function, label=arg_list[1]
                    )
                case self.CONDITIONAL_GOTO:
                    command = ConditionalGoToCommand(
                        function_name=self.current_function, label=arg_list[1]
                    )
                case self.FUNCTION:
                    self.current_function = arg_list[1]
                    self.call_count = 0
                    command = FunctionCommand(
                        function_name=self.current_function, local_number=arg_list[2]
                    )
                case self.CALL:
                    command = CallCommand(
                        function_name=arg_list[1],
                        arg_number=arg_list[2],
                        index=self.call_count,
                        current_function=self.current_function,
                    )
                    self.call_count += 1

        else:
            command = self.ARITHMETIC_MAP[arg_list[0]]

        return command
