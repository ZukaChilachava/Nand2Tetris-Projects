from dataclasses import dataclass


@dataclass
class DestinationConverter:
    line: str
    FIRST_SYMBOL: str = "A"
    SECOND_SYMBOL: str = "D"
    THIRD_SYMBOL: str = "M"

    PRESENT: str = "1"
    NOT_PRESENT: str = "0"

    def __convert_destination(self) -> str:
        first_symbol: str = self.__symbol(to_find=self.FIRST_SYMBOL)
        second_symbol: str = self.__symbol(to_find=self.SECOND_SYMBOL)
        third_symbol: str = self.__symbol(to_find=self.THIRD_SYMBOL)
        return first_symbol + second_symbol + third_symbol

    def __symbol(self, to_find: str) -> str:
        return self.NOT_PRESENT if str.find(self.line, to_find) == -1 else self.PRESENT

    def __str__(self) -> str:
        return self.__convert_destination()


@dataclass
class ComputationConverter:
    line: str
    NEUTRAL_SYMBOL: str = "N"
    A_OPERATION: str = "0"
    M_OPERATION: str = "1"
    MAP = {
        "0": "101010",
        "1": "111111",
        "-1": "111010",
        "D": "001100",
        "N": "110000",
        "!D": "001101",
        "!N": "110001",
        "-D": "001111",
        "-N": "110011",
        "D+1": "011111",
        "N+1": "110111",
        "D-1": "001110",
        "N-1": "110010",
        "D+N": "000010",
        "D-N": "010011",
        "N-D": "000111",
        "D&N": "000000",
        "D|N": "010101",
    }

    def __convert_computation(self) -> str:
        neutral_line: str = (self.line.replace("A", self.NEUTRAL_SYMBOL)).replace(
            "M", self.NEUTRAL_SYMBOL
        )

        return self.MAP.get(neutral_line, "")

    def __get_operation(self) -> str:
        return self.A_OPERATION if self.line.find("M") == -1 else self.M_OPERATION

    def __str__(self) -> str:
        return f"{self.__get_operation()}{self.__convert_computation()}"


@dataclass
class JumpConverter:
    line: str
    MAP = {
        "": "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111",
    }

    def __get_jump(self) -> str:
        return self.MAP.get(self.line, "")

    def __str__(self) -> str:
        return self.__get_jump()


@dataclass
class AInstructionConverter:
    CODE_WIDTH: int = 16

    def get_a_binary(self, line: str) -> str:
        return "{0:b}".format(int(line)).zfill(self.CODE_WIDTH)
