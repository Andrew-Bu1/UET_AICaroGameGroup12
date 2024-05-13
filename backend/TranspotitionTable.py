class TranspotitionTable:
    def __init__(self) -> None:
        self.table = {}

    def lookup(self, key):
        return self.table.get(key)

    def store(self, key, value):
        self.table[key] = value
