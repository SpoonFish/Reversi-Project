def initialise_board(size=8):
    """
    Creates a square Reversi board as a list of lists and returns it.

    Parameters:
        size (int): How many squares wide and tall the board is. Must be an even number between 4 and 16.

    Returns:
        list[list[str]]: 2D list of cells representing the board game. Each cell will be either "None ", "Dark ", or "Light".
    """

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

def legal_move(colour,coord,board):
    """
    Checks if a specified move follows the rules of the game and can be legally played.

    Parameters:
        colour (str): The colour of the counters of the player making the move.
        coord (tuple(int,int)): The x and y position of the counter being placed on the board for the move with x as the column number from the left and y as the row number from the top.
        board (list[list[str]]): The board containing the current status of each cell in the game.

    Returns:
        bool: Whether the move is legal or not.
    """

    x = coord[0] - 1
    y = coord[1] - 1
    target_space = board[y][x]
    size = len(board)
    if target_space != "None ":
        return False
    else:
        opposite_colour = "Dark " if colour == "Light" else "Light"
        valid_directions = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
        directions_to_remove = []
        for step in range(1,size):
            for d in directions_to_remove:
                valid_directions.remove(d)

            if len(valid_directions) == 0:
                break

            directions_to_remove.clear()

            for direction in valid_directions:
                dx = direction[0]*step
                dy = direction[1]*step

                if 0 > x+dx or x+dx >= size or 0 > y+dy or y+dy >= size: 
                    continue

                check_space = board[y + dy][x + dx]

                if step > 1 and check_space == colour:
                    return True
                if check_space != opposite_colour:
                    directions_to_remove.append(direction)
        return False



def print_board(board):
    """
    Prints the status of each cell on the board as empty, light or dark in a grid with row and column numbers.

    Parameters:
        board (list[list[str]]): The board containing the current status of each cell in the game.
    """
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