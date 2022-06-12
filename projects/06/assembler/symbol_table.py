class SymbolTable:
    INITIAL_INDEX: int = 16

    def __init__(self) -> None:
        self.variable_index: int = self.INITIAL_INDEX
        self.symbol_table = {
            "SP": 0,
            "LCL": 1,
            "ARG": 2,
            "THIS": 3,
            "THAT": 4,
            "SCREEN": 16384,
            "KBD": 24576,
        }
        for i in range(16):
            self.symbol_table[f"R{i}"] = i

    def add_label(self, label: str, index: int) -> None:
        self.symbol_table[label] = index

    def add_variable(self, var: str) -> None:
        self.symbol_table[var] = self.variable_index
        self.variable_index += 1

    def contains(self, symbol: str) -> bool:
        return False if self.symbol_table.get(symbol, None) is None else True

    def get_index(self, symbol: str) -> int:
        return self.symbol_table[symbol]
