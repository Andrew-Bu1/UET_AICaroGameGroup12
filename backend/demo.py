from TicTacToeAi import TicTacToeAi


def main():
    board = [
        ['x', 'o', 'x', ' ', 'x'],
        [' ', ' ', 'x', 'o', ' '],
        ['o', 'x', 'x', 'o', 'x'],
        ['x', 'x', 'o', 'o', 'o'],
        ['o', 'x', 'o', 'x', 'x'],
    ]

    ai = TicTacToeAi('x')
    move = ai.get_move(board)
    print(ai.evaluate())
    print(move)


if __name__ == "__main__":
    main()
