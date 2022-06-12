from typing import Iterable

from n2t.core.assembler.assembly_converter import (
    AInstructionConverter,
    ComputationConverter,
    DestinationConverter,
    JumpConverter,
)
from n2t.core.assembler.symbol_table import SymbolTable


class CodeParser:
    A_COMMAND: int = 0
    C_COMMAND: int = 1
    L_COMMAND: int = 2

    def __init__(self, assembly_code: Iterable[str]) -> None:
        self.formatted_string_array: list[str] = []
        self.assembly_code = assembly_code
        self.symbol_table: SymbolTable = SymbolTable()

    def parse_code(self) -> Iterable[str]:
        self.build_labels()
        return self.to_binary()

    def build_labels(self) -> None:
        instruction_index: int = 0
        for line in self.assembly_code:
            formatted_line: str = self.remove_whitespaces(line)
            if not self.is_valid_command(formatted_line):
                continue

            formatted_line = self.remove_inline_comments(formatted_line)

            command_type: int = self.get_command_type(formatted_line)
            if command_type == self.L_COMMAND:
                self.symbol_table.add_label(
                    label=CommandTokenizer.get_label(formatted_line),
                    index=instruction_index,
                )
                continue

            self.formatted_string_array.append(formatted_line)
            instruction_index += 1

    def to_binary(self) -> Iterable[str]:
        hack_code_array = []
        converter: AInstructionConverter = AInstructionConverter()
        for line in self.formatted_string_array:
            command_type: int = self.get_command_type(line)

            if command_type == self.C_COMMAND:
                dest: str = str(DestinationConverter(CommandTokenizer.get_dest(line)))
                comp: str = str(ComputationConverter(CommandTokenizer.get_comp(line)))
                jump: str = str(JumpConverter(CommandTokenizer.get_jump(line)))
                hack_code_array.append(f"{self.C_COMMAND}11{comp}{dest}{jump}")
            else:
                a_command: str = CommandTokenizer.get_a_command(line)
                if a_command[0].isdigit():
                    hack_code_array.append(converter.get_a_binary(a_command))
                    continue
                elif not self.symbol_table.contains(a_command):
                    self.symbol_table.add_variable(a_command)

                index: str = str(self.symbol_table.get_index(a_command))
                hack_code_array.append(converter.get_a_binary(index))

        return hack_code_array

    @staticmethod
    def remove_whitespaces(line: str) -> str:
        return line.replace(" ", "")

    @staticmethod
    def remove_inline_comments(line: str) -> str:
        comment_index: int = line.find("//")
        return line if comment_index == -1 else line[:comment_index]

    def get_command_type(self, line: str) -> int:
        a_or_c: int = self.A_COMMAND if line[0] == "@" else self.C_COMMAND
        return self.L_COMMAND if line[0] == "(" else a_or_c

    def is_valid_command(self, line: str) -> bool:
        is_not_empty: bool = False if len(line) == 0 else True
        return is_not_empty and not StringChecker.is_comment(line)


class CommandTokenizer:
    @staticmethod
    def get_dest(line: str) -> str:
        comp_index: int = line.find("=")
        return "" if comp_index == -1 else line[:comp_index]

    @staticmethod
    def get_comp(line: str) -> str:
        start_index: int = line.find("=") + 1
        index_of_jump: int = line.find(";")
        end_index: int = line.__len__() if index_of_jump == -1 else index_of_jump
        return line[start_index:end_index]

    @staticmethod
    def get_jump(line: str) -> str:
        index: int = line.find(";") + 1
        return "" if index == 0 else line[index:]

    @staticmethod
    def get_label(line: str) -> str:
        left_index: int = line.find("(") + 1
        right_index: int = line.rfind(")")
        return line[left_index:right_index]

    @staticmethod
    def get_a_command(line: str) -> str:
        command_index: int = line.find("@") + 1
        return line[command_index:]


class StringChecker:
    @staticmethod
    def is_comment(line: str) -> bool:
        return line[0] == "/" and line[1] == "/"
