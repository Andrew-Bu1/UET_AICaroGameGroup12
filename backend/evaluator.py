import constant as const
from typing import Literal

def evaluate(board: list[list[str]], playerRole: Literal['x', 'o']):
    score = 0
    size = len(board)
        # Check Rows
    for i in range(size):
        temp = evaluate_line([board[i][j]
                                    for j in range(size)], playerRole)
        if (abs(temp) == const.FIVE):
            return temp
        score += temp

    # Check Columns
    for j in range(size):
        temp = evaluate_line([board[i][j]
                                    for i in range(size)], playerRole)
        if (abs(temp) == const.FIVE):
            return temp
        score += temp

    # Check Diagonal from left to right and from the top to the bottom
    for i in range(1, size - const.MAX_CONNECT + 1):
        temp = evaluate_line([board[i + j][j]
                                    for j in range(size - i)], playerRole)
        if (abs(temp) == const.FIVE):
            return temp
        score += temp

    for i in range(size - const.MAX_CONNECT + 1):
        temp = evaluate_line([board[j][i + j]
                                    for j in range(size - i)], playerRole)
        if (abs(temp) == const.FIVE):
            return temp
        score += temp

    # Check Diagonal from left to right and bottom to the top
    for i in range(1, size - const.MAX_CONNECT + 1):
        temp = evaluate_line(
            [board[size - (i + j + 1)][j] for j in range(size - i)], playerRole)
        if (abs(temp) == const.FIVE):
            return temp
        score += temp

    for i in range(size - const.MAX_CONNECT + 1):
        temp = evaluate_line([board[size - j - 1][i + j]
                                    for j in range(size - i)], playerRole)
        if (abs(temp) == const.FIVE):
            return temp
        score += temp

    return score

def evaluate_line(line: list[str], playerRole: Literal['x', 'o']):
    score = 0
    player_cnt, opponent_cnt = 0, 0
    oppentRole = 'o' if playerRole == 'x' else 'x'
    queue = []
    

    for element in line:
        queue.append(element)
        if element == playerRole:
            player_cnt += 1
            if opponent_cnt > 0:
                opponent_cnt = 0
        if element == oppentRole:
            opponent_cnt += 1
            if player_cnt > 0:
                player_cnt = 0

        if len(queue) == const.MAX_CONNECT:
            if player_cnt == const.MAX_CONNECT:
                return const.PLAYER_WIN_SCORE
            elif opponent_cnt == const.MAX_CONNECT:
                return const.OPPONENT_WIN_SCORE
            else:
                if player_cnt > 1 :
                    score += const.SCORE[player_cnt]
                elif opponent_cnt > 1:
                    score -= const.SCORE[opponent_cnt]
            temp = queue.pop(0)
            if temp == playerRole:
                player_cnt -= 1
            elif temp == oppentRole:
                opponent_cnt -= 1

    return score
