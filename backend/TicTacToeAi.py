import time
import numpy as np
import constant as const
from evaluator import evaluate
from OpeningMoves import first_move

class TicTacToeAi:
    def __init__(self, role) -> None:
        """
        Args:
            role (_type_): Role of the player (x or o)
        """
        self.size = 0
        self.board = list[list[str]]
        self.max_connect = const.MAX_CONNECT
        self.first_move = True
        self.move_left = []
        self.transposition_table = {}
        self.zobrist_table = np.random.randint(2**64, size=(15, 15, 2), dtype=np.uint64)
        self.hash = np.uint64(0)
         

        self.playerRole = role
        if self.playerRole == const.X_CELL:
            self.opponentRole = const.O_CELL
        else:
            self.opponentRole = const.X_CELL

    def set_first_move(self):
        self.first_move = False
    
    def update_zobrist_hash(self, move, number):
            self.hash ^= np.uint64(self.zobrist_table[move[0]][move[1]][number])
    
    def make_move(self, move, cell):
        self.board[move[0]][move[1]] = cell
        temp = 0 if cell == self.playerRole else 1
        self.update_zobrist_hash(move, temp)
        self.move_left.remove(move)
        
    def unmake_move(self, move, cell):
        self.board[move[0]][move[1]] = const.EMPTY_CELL
        temp = 0 if cell == self.playerRole else 1
        self.update_zobrist_hash(move, temp)
        self.move_left.append(move)
        
    
    def generate_moves(self):
        self.move_left = [
            [i, j] for i in range(self.size) for j in range(self.size) if self.board[i][j] == const.EMPTY_CELL
        ]

    def get_move(self, board) -> tuple[int, int]:
        if self.first_move:
            self.first_move = False
            return first_move(board, self.playerRole)
        else:
            bestMove = [-1, -1]
            self.board = board
            self.size = len(board)
        
            bestVal = const.MIN_VALUE
            beta = const.MIN_VALUE
            self.generate_moves()

            for move in self.move_left:
                self.make_move(move, self.playerRole)
                moveScore = self.min_search(
                    bestVal, beta, depth=0)

                self.unmake_move(move, self.playerRole)

                if moveScore > bestVal:
                    bestMove = [move[0], move[1]]
                    bestVal = moveScore

            return bestMove


    def min_search(self, alpha, beta, depth) -> int:
        if self.hash in self.transposition_table:
            return self.transposition_table[self.hash]
            
        score = evaluate(self.board, self.playerRole)
    
        if (depth == const.MAX_DEPTH or score == const.PLAYER_WIN_SCORE or score == const.OPPONENT_WIN_SCORE):
            return score
        
        val = const.MAX_VALUE

        for move in self.move_left:
            self.make_move(move, self.opponentRole)
            val = min(val, self.max_search(alpha, beta, depth + 1))
            
            self.unmake_move(move, self.opponentRole)
            if val <= alpha:
                return val
            beta = min(beta, val)
            self.transposition_table[self.hash] = val
        return val
    
    def max_search(self, alpha, beta, depth) -> int:
        if self.hash in self.transposition_table:
            return self.transposition_table[self.hash]

        score = evaluate(self.board, self.playerRole)
    
        if (depth == const.MAX_DEPTH or score == const.PLAYER_WIN_SCORE or score == const.OPPONENT_WIN_SCORE):
            return score
    
        val = const.MIN_VALUE
        
        for move in self.move_left:
            i, j = move
            self.board[i][j] = self.playerRole
            self.move_left.remove(move)
            val = max(val, self.min_search(alpha, beta, depth + 1))
            
            self.board[i][j] = const.EMPTY_CELL
            self.move_left.append(move)
            if val >= beta:
                return val
            alpha = max(alpha, val)
            self.transposition_table[self.hash] = val
        return val
    
    
