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

    # def get_move(self, board):
    #     self.board = board
    #     self.size = len(board)

    #     win = self.evaluate()
    #     if abs(win) == const.WIN_SCORE:
    #         return None
    #     res = self.search_best_move()

    def get_move(self, board) -> tuple[int, int]:
        bestMove = [-1, -1]
        bestVal = const.MIN_VALUE
        self.board = board
        self.size = len(board)

        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == ' ':
                    self.board[i][j] = self.playerRole

                    moveScore = self.minimax(
                        0, False, const.MIN_VALUE, const.MAX_VALUE)

                    self.board[i][j] = ' '

                    if moveScore > bestVal:
                        bestMove[0] = i
                        bestMove[1] = j
                        bestVal = moveScore

        return bestMove

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

        return score

    def minimax(self, depth, isMax: bool, alpha: int, beta: int) -> int:
        score = self.evaluate()

        if depth == 5 or score == const.PLAYER_WIN_SCORE:
            return score

        if score == const.OPPONENT_WIN_SCORE:
            return score

        if isMax:
            best = const.MIN_VALUE

            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.playerRole
                        best = max(best, self.minimax(
                            depth + 1, not isMax, alpha, beta)) - depth * 5
                        self.board[i][j] = ' '
                        if best > beta:
                            break

            return best
        else:
            best = const.MAX_VALUE

            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.opponentRole
                        best = min(best, self.minimax(
                            depth+1, not isMax, alpha, beta)) + depth * 5
                        self.board[i][j] = ' '
                        beta = min(beta, best)
                        if best < alpha:
                            break

            return best
