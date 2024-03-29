class SymbolTable:
    def __init__(self) -> None:
        self.table = {}
        self.initialize_table()

    def initialize_table(self):
        self.table = {f"R{i}": i for i in range(16)}
        self.table["SCREEN"] = 16384
        self.table["KBD"] = 24576
        self.table["SP"] = 0
        self.table["LCL"] = 1
        self.table["ARG"] = 2
        self.table["THIS"] = 3
        self.table["THAT"] = 4
    
    def add_symbol(self, symbol, address):
        self.table[symbol] = address
