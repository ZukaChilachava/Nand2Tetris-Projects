from typing import Protocol


class VMCommand(Protocol):
    def get_command(self) -> str:
        pass


class ArgCommand(Protocol):
    def get_command(self, arg: str) -> str:
        pass
