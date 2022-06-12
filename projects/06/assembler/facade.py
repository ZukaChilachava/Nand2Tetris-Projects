from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from n2t.core.assembler.code_parser import CodeParser


@dataclass
class Assembler:
    @classmethod
    def create(cls) -> Assembler:
        return cls()

    def assemble(self, assembly: Iterable[str]) -> Iterable[str]:
        cd: CodeParser = CodeParser(assembly_code=assembly)
        return cd.parse_code()
