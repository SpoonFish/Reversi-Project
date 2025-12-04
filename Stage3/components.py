"""
Utility functions for the game Reversi. Includes board initialisation,
legal move checking, and board representation printing.
"""

def initialise_board(size=8):
    """
    Creates a square Reversi board as a list of lists and returns it.

    Parameters:
        size (int): How many squares wide and tall the board is.
        Must be an even number between 4 and 16.

    Returns:
        list[list[str]]: 2D list of cells representing the board game.
        Each cell will be either "None ", "Dark ", or "Light".
    """

    # Check the value of the 'size' parameter is valid and appropriate
    # for being the width and height of the board
    if not isinstance(size, int):
        raise TypeError("Board size must be an integer.")
    if size % 2 != 0:
        raise ValueError("Board size must be an even integer.")
    if size < 4:
        raise ValueError("Board size must be 4 or above")
    if size > 16:
        raise ValueError("Board size must be 16 or below.")

    board = []

    # Fill the board with rows of the string "None "
    for _ in range(size):
        board.append(["None " for _ in range(size)])

    # Set the middle 4 squares of the board as an alternating pattern of "Dark " and "Light"
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
        coord (tuple(int,int)): The x and y position of the counter being placed on the board.
            x is the column number from the left and y as the row number from the top.
        board (list[list[str]]): The board containing the current status of each cell in the game.

    Returns:
        bool: Whether the move is legal or not.
    """

    # Reduce values in the coordinate tuple by 1 so that they translate to
    # zero-based indices of the board lists
    x = coord[0] - 1
    y = coord[1] - 1

    # Get the state of the cell at the desired position for the move
    target_cell = board[y][x]

    size = len(board)

    # The move cannot be legal if the cell is already occupied by any counter
    if target_cell != "None ":
        return False

    # Get the opposite colour to the colour of the player making the move
    opposite_colour = "Dark " if colour == "Light" else "Light"

    # Stores a set of directions vectors which will act as displacements
    # from the position of the move to check if the states of the surrounding cells
    # allow the move to be legal
    valid_directions = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]

    directions_to_remove = []

    # Search the surrounding cells outwards in direct straight lines
    # from the specified move position
    for step in range(1,size):

        # Remove all the direction vectors that are confirmed to lead to invalid moves
        # from the previous iteration before checking the next surrounding cells
        for d in directions_to_remove:
            valid_directions.remove(d)

        # No directions of search can lead to a possible legal move from the specified position
        # so exit the search
        if len(valid_directions) == 0:
            break

        # Reset the list so that directions are not removed twice
        directions_to_remove.clear()

        for direction in valid_directions:
            # Get the change in position from x and y to calculate
            # the position of the cell being checked
            dx = direction[0]*step
            dy = direction[1]*step

            # Do not check the cell if the position to be searched is outside the board
            if 0 > x+dx or x+dx >= size or 0 > y+dy or y+dy >= size:
                continue

            # The status of the cell being checked
            check_cell = board[y + dy][x + dx]

            # There is a counter of the same colour in a straight line from
            # the desired position that has at least 1 counter of the opposite colour
            # between them,so the move is legal
            if step > 1 and check_cell == colour:
                return True

            # This checks if an empty cell is reached before reaching a cell of
            # the current player's colour, if there is then this direction of search will
            # not lead to any legal moves

            # It also checks if the cell adjacent to the desired position in the current
            # direction is the same colour as the current player's colour.
            # This would lead to no counters of the opposite colour ending up between the
            # desired position and the next counter of the same colour in a line
            # so the current direction would lead to no legal moves
            if check_cell != opposite_colour:
                directions_to_remove.append(direction)
    return False



def print_board(board):
    """
    Prints the status of each cell on the board as empty, light or dark
    in a grid with row and column numbers.

    Parameters:
        board (list[list[str]]): The board containing the current status of each cell in the game.
    """
    size = len(board)

    # Padding for the top left corner of the representation
    print(end="   ")

    # Print the column numbers so that they are
    # directly above the column they are associated with
    for i in range(size):
        # Numbers with 2 digits need less padding
        if i+1 < 10:
            print(i+1, end="     ")
        else:
            print(i+1, end="    ")

    # Start the printing of rows on a new line
    print()

    # Print the row number along with the status of each cell in the row
    for i, row in enumerate(board):
        # Numbers with 2 digits need less padding
        if i+1 < 10:
            print(i+1, end="  ")
        else:
            print(i+1, end=" ")

        for cell in row:
            print(cell, end=" ")

        # Print a new line so rows are not all printed on the same line
        print()
