import numpy as np
from typing import Literal
class TranspositionTable(object):
    
    def __init__(self) -> None:
        self.table = {}
        
    def store(self, code, score):
        self.table[code] = score
        
    def lookup(self, code):
        return self.table.get(code)
    
class ZobristTable:
        
    def __init__(self, size) -> None:
        self.zobrist_table = np.random.randint(2**64, size=(size, size, 2), dtype=np.uint64)
        self.hash = np.uint64(0)
        
    def update_table(self, move, player):
        x, y = move
        self.hash ^= self.zobrist_table[x][y][player]
        