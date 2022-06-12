from dataclasses import dataclass
from typing import Iterable

from n2t.core.vm_translator.vm_parser import VMParser


@dataclass
class VMTranslator:
    def translate(self, file_name: str, vm_code: Iterable[str]) -> Iterable[str]:
        return VMParser(file_name=file_name, vm_code=vm_code).parse_code()
