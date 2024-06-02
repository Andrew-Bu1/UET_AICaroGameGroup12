import numpy as np
import sys
import time
import concurrent.futures

class Gomoku:
    def __init__(self, size=15):
        self.size = size
        self.board = np.zeros((size, size), dtype=int)  # 0 = empty, 1 = player 1, 2 = player 2
        self.zobrist_table = np.random.randint(2**64, size=(size, size, 3), dtype=np.uint64)  # 3 for empty, player 1, player 2
        self.hash = np.uint64(0)
        self.transposition_table = {}
    
    def make_move(self, x, y, player):
        self.board[x, y] = player
        self.hash ^= self.zobrist_table[x, y, player]

    def unmake_move(self, x, y, player):
        self.board[x, y] = 0
        self.hash ^= self.zobrist_table[x, y, player]

    def is_winner(self, player):
        # Check for five in a row for the given player
        pass  # Implement the win condition check

def evaluate(gomoku):
    # Implement an evaluation function for the current board state
    score = 0
    # Example: Simple heuristic
    for row in range(gomoku.size):
        for col in range(gomoku.size):
            if gomoku.board[row, col] == 1:
                score += 1
            elif gomoku.board[row, col] == 2:
                score -= 1
    return score

def generate_moves(gomoku):
    # Generate all possible moves
    moves = []
    for x in range(gomoku.size):
        for y in range(gomoku.size):
            if gomoku.board[x, y] == 0:
                moves.append((x, y))
    return moves

def alpha_beta(gomoku, depth, alpha, beta, maximizing_player):
    # Check if the current board state is in the transposition table
    if gomoku.hash in gomoku.transposition_table:
        return gomoku.transposition_table[gomoku.hash]

    if depth == 0 or gomoku.is_winner(1) or gomoku.is_winner(2):
        evaluation = evaluate(gomoku)
        gomoku.transposition_table[gomoku.hash] = evaluation
        return evaluation

    if maximizing_player:
        max_eval = -sys.maxsize
        for move in generate_moves(gomoku):
            gomoku.make_move(move[0], move[1], 1)
            eval = alpha_beta(gomoku, depth-1, alpha, beta, False)
            gomoku.unmake_move(move[0], move[1], 1)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        gomoku.transposition_table[gomoku.hash] = max_eval
        return max_eval
    else:
        min_eval = sys.maxsize
        for move in generate_moves(gomoku):
            gomoku.make_move(move[0], move[1], 2)
            eval = alpha_beta(gomoku, depth-1, alpha, beta, True)
            gomoku.unmake_move(move[0], move[1], 2)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        gomoku.transposition_table[gomoku.hash] = min_eval
        return min_eval

def iterative_deepening(gomoku, max_depth, time_limit):
    start_time = time.time()
    best_move = None

    for depth in range(1, max_depth + 1):
        if time.time() - start_time > time_limit:
            break
        best_move = parallel_alpha_beta(gomoku, depth, -sys.maxsize, sys.maxsize, True, time_limit - (time.time() - start_time))
    return best_move

def parallel_alpha_beta(gomoku, depth, alpha, beta, maximizing_player, time_limit):
    start_time = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for move in generate_moves(gomoku):
            if time.time() - start_time > time_limit:
                break
            gomoku.make_move(move[0], move[1], 1 if maximizing_player else 2)
            futures.append(executor.submit(alpha_beta_parallel_wrapper, gomoku, depth-1, alpha, beta, not maximizing_player, gomoku.hash))
            gomoku.unmake_move(move[0], move[1], 1 if maximizing_player else 2)
        
        best_score = -sys.maxsize if maximizing_player else sys.maxsize
        best_move = None
        for future in concurrent.futures.as_completed(futures):
            move, score = future.result()
            if (maximizing_player and score > best_score) or (not maximizing_player and score < best_score):
                best_score = score
                best_move = move
    return best_move

def alpha_beta_parallel_wrapper(gomoku, depth, alpha, beta, maximizing_player, zobrist_hash):
    # Clone the game state based on the hash
    cloned_gomoku = Gomoku(gomoku.size)
    cloned_gomoku.board = np.copy(gomoku.board)
    cloned_gomoku.hash = zobrist_hash
    cloned_gomoku.transposition_table = gomoku.transposition_table

    best_score = alpha_beta(cloned_gomoku, depth, alpha, beta, maximizing_player)
    return (None, best_score)  # Return None for move, as it's not needed in this context
