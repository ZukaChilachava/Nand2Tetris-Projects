import os
from dataclasses import dataclass
from typing import Iterable

from n2t import definitions
from n2t.core.string.string_utilities import StringUtil
from n2t.core.vm_translator.command_checker import CommandChecker
from n2t.core.vm_translator.command_protocols import VMCommand


@dataclass
class VMParser:
    file_name: str
    vm_code: Iterable[str]

    def parse_code(self) -> list[str]:
        command_checker: CommandChecker = CommandChecker(file_name=self.file_name)
        result: str = ""

        for line in self.vm_code:
            new_line: str = StringUtil.remove_whitespaces(line)

            if len(new_line) == 0 or StringUtil.is_comment(new_line):
                continue

            parsed_cmd = StringUtil.remove_inline_comments(line)

            command: VMCommand = command_checker.get_command_type(line=parsed_cmd)
            command_in_assembler: str = command.get_command()
            # result += f"//{line}\n"
            result += command_in_assembler + "\n"

        return result.splitlines()


if __name__ == "__main__":
    print(
        os.path.join(os.path.dirname(definitions.N2T_DIRECTORY), "tests", "e2e", "vm")
    )
