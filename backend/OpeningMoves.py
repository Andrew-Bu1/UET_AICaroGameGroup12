# class OpeningMoves:
#     def __init__(self, size) -> None:
        
#         self.openings = {
#             "first": [(size // 2, size // 2)],
#             "second": [(size // 2 + 1, size // 2 + 1)],
#         }
        
#     def get_opening_move(self, move_number, first_move = None):
#         if move_number == 0:
#             return self.openings["first"]
#         elif move_number == 1:
#             return self.openings["second"]            
#         else: 
#             return None
        
        
def first_move(board: list[list[str]], role) -> tuple[int, int]:
    size = len(board)
    if (role == 'x'):
        return (size // 2, size // 2)
    else:
        for i in range(size):
            for j in range(size):
                if (board[i][j] == 'x'):
                    if (i + 1  < size and j + 1 < size):
                        return [i + 1, j + 1]
                    elif (i - 1 > 0 and j - 1 > 0):
                        return [i - 1, j - 1]
                    elif (i + 1 < size and j - 1 > 0):
                        return [i + 1, j - 1]
                    elif (i - 1 > 0 and j + 1 < size):
                        return [i - 1, j - 1]
    