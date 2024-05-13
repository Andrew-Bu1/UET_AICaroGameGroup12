import copy
import random
import constant as const


class TicTacToeAi:
    def __init__(self, role) -> None:
        """
        Args:
            role (_type_): Role of the player (x or o)
        """
        self.size = 0
        self.board = list[list[str]]
        self.max_connect = const.MAX_CONNECT

        self.playerRole = role

        if self.playerRole == 'x':
            self.opponentRole = 'o'
        else:
            self.opponentRole = 'x'

    def get_move(self, board):
        self.board = board
        self.size = len(board)

    def evaluate(self) -> int:
        score = 0

        # Check Rows
        for i in range(self.size):
            temp = self.evaluate_line([self.board[i][j]
                                      for j in range(self.size)])
            if (abs(temp) == const.WIN_SCORE):
                return temp
            score += temp

        # Check Columns
        for j in range(self.size):
            temp = self.evaluate_line([self.board[i][j]
                                      for i in range(self.size)])
            if (abs(temp) == const.WIN_SCORE):
                return temp
            score += temp

        # Check Diagonal from left to right and from the top to the bottom
        for i in range(1, self.size - self.max_connect + 1):
            temp = self.evaluate_line([self.board[i + j][j]
                                      for j in range(self.size - i)])
            if (abs(temp) == const.WIN_SCORE):
                return temp
            score += temp

        for i in range(self.size - self.max_connect + 1):
            temp = self.evaluate_line([self.board[j][i + j]
                                      for j in range(self.size - i)])
            if (abs(temp) == const.WIN_SCORE):
                return temp
            score += temp

        # Check Diagonal from left to right and bottom to the top
        for i in range(1, self.size - self.max_connect + 1):
            temp = self.evaluate_line(
                [self.board[self.size - (i + j + 1)][j]] for j in range(self.size - i))
            if (abs(temp) == const.WIN_SCORE):
                return temp
            score += temp

        for i in range(self.size - self.max_connect + 1):
            temp = self.evaluate_line([self.board[self.size - j - 1][i + j]
                                      for j in range(self.size - i)])
            if (abs(temp) == const.WIN_SCORE):
                return temp
            score += temp

        return score

    def evaluate_line(self, line) -> int:
        score = 0
        queue = []
        player_cnt, opponent_cnt = 0, 0

        for element in line:
            queue.append(element)
            if element == self.playerRole:
                player_cnt += 1
                if opponent_cnt > 0:
                    opponent_cnt = 0
            if element == self.opponentRole:
                opponent_cnt += 1
                if player_cnt > 0:
                    player_cnt = 0

            if len(queue) == self.max_connect:
                if player_cnt == self.max_connect:
                    return const.PLAYER_WIN_SCORE
                elif opponent_cnt == self.max_connect:
                    return const.OPPONENT_WIN_SCORE
                else:
                    if player_cnt > 0:
                        score += pow(10, player_cnt - 1)
                    elif opponent_cnt > 0:
                        score -= pow(10, opponent_cnt - 1)
                queue.pop(0)
                # temp = queue.pop(0)
                # if temp == self.playerRole:
                #     player_cnt -= 1
                # elif temp == self.opponentRole:
                #     opponent_cnt -= 1

        return score

    def minimax(self, depth, alpha: float, beta: float):
        score: int
        bestRow = -1
        bestCol = -1

        if (depth == 0):
            score = self.evaluate()
        else:
            return
        return
