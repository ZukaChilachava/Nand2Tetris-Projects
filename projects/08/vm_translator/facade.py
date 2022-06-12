from dataclasses import dataclass
from typing import Iterable

from n2t.core.vm_translator.file_merger.file_translator import (
    BootstrapTranslator,
    DefaultTranslator,
    FileTranslator,
)


@dataclass
class VMTranslator:
    def translate(
        self, file_name: str, vm_code: dict[str, Iterable[str]], is_file: bool
    ) -> Iterable[str]:
        merger: FileTranslator
        if is_file:
            merger = DefaultTranslator(file_name=file_name, file_list=vm_code)
        else:
            merger = BootstrapTranslator(file_name=file_name, file_list=vm_code)

        result: list[str] = merger.translate_files()

        return result
