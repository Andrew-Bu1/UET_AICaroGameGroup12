# def get_diagonals(matrix, length):
#     """
#     Get all the diagonals of a matrix with a given length, excluding the main diagonal.
#     """
#     diagonals = []

#     # Get number of rows and columns in the matrix
#     rows = len(matrix)
#     cols = len(matrix[0])

#     for i in range(1, rows - length + 1):  # Start from index 1 to skip main diagonal
#         diagonal = []
#         for j in range(rows - i):
#             diagonal.append(matrix[i + j][j])
#         diagonals.append(diagonal)

#     # Iterate through diagonals starting from the top-right corner
#     for i in range(cols - length + 1):
#         diagonal = []
#         for j in range(cols - i):
#             diagonal.append(matrix[j][i + j])
#         diagonals.append(diagonal)

#     # Iterate through diagonals starting from the top-left corner
#     for i in range(1, rows - length + 1):  # Start from index 1 to skip main diagonal
#         diagonal = []
#         for j in range(rows - i):
#             diagonal.append(matrix[rows - (i + j) - 1][j])
#         diagonals.append(diagonal)

#     # Iterate through diagonals starting from the top-right corner
#     for i in range(cols - length + 1):
#         diagonal = []
#         for j in range(cols - i):
#             diagonal.append(matrix[rows - j - 1][i + j])
#         diagonals.append(diagonal)

#     return diagonals


# # Example usage
# matrix = [
#     [1, 2, 3, 4, 5],
#     [6, 7, 8, 9, 10],
#     [11, 12, 13, 14, 15],
#     [16, 17, 18, 19, 20],
#     [21, 22, 23, 24, 25]
# ]

# length = 5  # Length of diagonals
# diagonals = get_diagonals(matrix, length)
# print("Diagonals of length 6 in the matrix (excluding main diagonal):")
# for diagonal in diagonals:
#     print(diagonal)
# Python3 program to find the next optimal move for a player
player, opponent = 'x', 'o'

# This function returns true if there are moves
# remaining on the board. It returns false if
# there are no moves left to play.


def isMovesLeft(board):

    for i in range(3):
        for j in range(3):
            if (board[i][j] == '_'):
                return True
    return False

# This is the evaluation function as discussed
# in the previous article ( http://goo.gl/sJgv68 )


def evaluate(b):

    # Checking for Rows for X or O victory.
    for row in range(3):
        if (b[row][0] == b[row][1] and b[row][1] == b[row][2]):
            if (b[row][0] == player):
                return 10
            elif (b[row][0] == opponent):
                return -10

    # Checking for Columns for X or O victory.
    for col in range(3):

        if (b[0][col] == b[1][col] and b[1][col] == b[2][col]):

            if (b[0][col] == player):
                return 10
            elif (b[0][col] == opponent):
                return -10

    # Checking for Diagonals for X or O victory.
    if (b[0][0] == b[1][1] and b[1][1] == b[2][2]):

        if (b[0][0] == player):
            return 10
        elif (b[0][0] == opponent):
            return -10

    if (b[0][2] == b[1][1] and b[1][1] == b[2][0]):

        if (b[0][2] == player):
            return 10
        elif (b[0][2] == opponent):
            return -10

    # Else if none of them have won then return 0
    return 0

# This is the minimax function. It considers all
# the possible ways the game can go and returns
# the value of the board


def minimax(board, depth, isMax):
    score = evaluate(board)

    # If Maximizer has won the game return his/her
    # evaluated score
    if (score == 10):
        return score

    # If Minimizer has won the game return his/her
    # evaluated score
    if (score == -10):
        return score

    # If there are no more moves and no winner then
    # it is a tie
    if (isMovesLeft(board) == False):
        return 0

    # If this maximizer's move
    if (isMax):
        best = -1000

        # Traverse all cells
        for i in range(3):
            for j in range(3):

                # Check if cell is empty
                if (board[i][j] == '_'):

                    # Make the move
                    board[i][j] = player

                    # Call minimax recursively and choose
                    # the maximum value
                    best = max(best, minimax(board,
                                             depth + 1,
                                             not isMax))

                    # Undo the move
                    board[i][j] = '_'
        return best

    # If this minimizer's move
    else:
        best = 1000

        # Traverse all cells
        for i in range(3):
            for j in range(3):

                # Check if cell is empty
                if (board[i][j] == '_'):

                    # Make the move
                    board[i][j] = opponent

                    # Call minimax recursively and choose
                    # the minimum value
                    best = min(best, minimax(board, depth + 1, not isMax))

                    # Undo the move
                    board[i][j] = '_'
        return best

# This will return the best possible move for the player


def findBestMove(board):
    bestVal = -1000
    bestMove = (-1, -1)

    # Traverse all cells, evaluate minimax function for
    # all empty cells. And return the cell with optimal
    # value.
    for i in range(3):
        for j in range(3):

            # Check if cell is empty
            if (board[i][j] == '_'):

                # Make the move
                board[i][j] = player

                # compute evaluation function for this
                # move.
                moveVal = minimax(board, 0, False)

                # Undo the move
                board[i][j] = '_'

                # If the value of the current move is
                # more than the best value, then update
                # best/
                if (moveVal > bestVal):
                    bestMove = (i, j)
                    bestVal = moveVal

    print("The value of the best Move is :", bestVal)
    print()
    return bestMove


# Driver code
board = [
        ['x', 'o', 'x'],
        ['x', 'o', 'o'],
        ['_', '_', '_']
]

bestMove = findBestMove(board)

print("The Optimal Move is :")
print("ROW:", bestMove[0], " COL:", bestMove[1])

# This code is contributed by divyesh072019
