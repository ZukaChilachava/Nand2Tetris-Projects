from dataclasses import dataclass
from typing import Iterable, Protocol

from n2t.core.vm_translator.command_processors.function_commands import CallCommand
from n2t.core.vm_translator.commands import StaticCommands
from n2t.core.vm_translator.vm_parser import VMParser


class FileTranslator(Protocol):
    def translate_files(self) -> list[str]:
        pass


@dataclass
class DefaultTranslator:
    file_name: str
    file_list: dict[str, Iterable[str]]

    def translate_files(self) -> list[str]:
        result_list: list[str] = []

        for file_name, file_content in self.file_list.items():
            result_list += VMParser(
                file_name=file_name, vm_code=file_content
            ).parse_code()

        return result_list


class BootstrapTranslator:
    def __init__(self, file_name: str, file_list: dict[str, Iterable[str]]):
        self.file_name = file_name
        self.file_list = file_list

    def translate_files(self) -> list[str]:
        result_list: list[str] = DefaultTranslator(
            file_name=self.file_name, file_list=self.file_list
        ).translate_files()
        call_sys_init: str = CallCommand(
            arg_number="0", current_function="", function_name="Sys.init", index=0
        ).get_command()
        result_list = (
            StaticCommands.set_bootstrap_stack().splitlines()
            + call_sys_init.splitlines()
            + result_list
        )
        return result_list
