def initialise_board(size=8):
    if not isinstance(size, int):
        raise TypeError("Board size must be an integer.")
    if size % 2 != 0:
        raise ValueError("Board size must be an even integer.")
    if size < 4:
        raise ValueError("Board size must be 4 or above")
    if size > 16:
        raise ValueError("Board size must be 16 or below.")
    
    board = []

    for _ in range(size):
        board.append(["None " for _ in range(size)])

    board[size//2][size//2] = "Dark "
    board[size//2-1][size//2-1] = "Dark "
    board[size//2-1][size//2] = "Light"
    board[size//2][size//2-1] = "Light"

    return board

def legal_move():
    for row in board:
        for space in row:
            if space != "None ":
                return False
            else:
                valid = False
                opposite_colour = "Dark " if space == "Light" else "Light"
                for x in 

def print_board(board):
    size = len(board)
    print(end="   ")
    for i in range(size):
        if i+1 < 10:
            print(i+1, end="     ")
        else:
            print(i+1, end="    ")
    print()
    for i, row in enumerate(board):
        if i+1 < 10:
            print(i+1, end="  ")
        else:
            print(i+1, end=" ")
        for space in row:
            print(space, end=" ")
        print()

board = initialise_board()
print_board(board)