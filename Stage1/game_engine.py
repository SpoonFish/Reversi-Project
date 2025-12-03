"""
CLI version of Reversi.

Handles user input and executes the main game loop. Each turn it validates the
moves entered by the player, updates the board with the chosen move and switches turn.
At the end of the game the winner is determined and displayed then the game is exited.
The 'components' module used for board creation, printing, and legal move checks.
"""

import components

BOARD_SIZE = 8

def cli_input_coords():
    """
    Requests column and row number of the cell the player wants to place a counter on until
    valid numbers are inputted.

    Returns:
        tuple(int,int): The x and y position of the players desired move.
    """

    # Keep asking the player for a move position until a valid move is given
    while True:
        x = input("Enter x coordinate of move: ")
        y = input("Enter y coordinate of move: ")

        # Checks inputted coordinates are whole positive numbers
        if not x.isdecimal() or not y.isdecimal():
            print("Coordinates must both be whole numbers. Try again")
            continue

        # Disallow numbers longer than necessary to avoid extremely long digit numbers
        # that cause str to int conversion to error (>4300 digit numbers)
        if len(x) > 2 or len(y) > 2:
            print("Inputted numbers are too long. Try again")
            continue

        # They are safe to convert into integers now
        x = int(x)
        y = int(y)

        # Check the coordinates are on the board
        if x < 1 or y < 1 or x > BOARD_SIZE or y > BOARD_SIZE:
            print(f"Coordinates must be whole numbers within 1 and {BOARD_SIZE}")
            continue

        return (x, y)

def simple_game_loop():
    """
    Initialises the game, processes the players' moves and ends the game . 
    """

    print("Welcome to CLI Reversi! :)")

    # Initialise the board and some variables used throughout the whole game
    board = components.initialise_board(BOARD_SIZE)
    move_counter = 60
    current_player_colour = "Dark "
    game_won = False
    previous_turn_passed = False

    # Print the initial board so the player can see what moves are available easily
    components.print_board(board)

    while not game_won:
        # Check there is a legal move for the current player
        has_legal_move = False
        for y, row in enumerate(board):
            for x, cell in enumerate(row):
                if cell != "None ":
                    continue

                # If there is at least one legal move to make,
                # then the player must continue with their turn
                if components.legal_move(current_player_colour, (x+1, y+1), board):
                    has_legal_move = True

        # Change players if there are no legal moves and display this to the player
        # to let them know their turn is passed
        if not has_legal_move:
            # Toggles player
            current_player_colour = "Dark " if current_player_colour == "Light" else "Light"

            print(f"{current_player_colour.strip()} has no legal moves! Passing turn")

            # If the previous turn was also passed that means neither player
            # can make a legal moveso the game is over
            if previous_turn_passed:
                print("No more legal moves can be made by either player. Game over!")
                game_won = True

            previous_turn_passed = True
            continue

        # Reset this to False because there is a move that can be made
        previous_turn_passed = False

        print(f"{move_counter} max moves left")
        print(f"Its {current_player_colour.strip()}'s turn")

        move = (0, 0)

        # Requests a move from the player and checks if it is legal
        # The player has to enter a legal move for the turn to progress
        while True:
            move = cli_input_coords()
            if components.legal_move(current_player_colour, move, board):
                break
            print("Move is invalid. Try again")

        move_counter -= 1

        # Convert move position to list indices
        x = move[0] - 1
        y = move[1] - 1

        # Set the cell selected by the player to a counter of their colour
        board[y][x] = current_player_colour

        # Stores a set of directions vectors which will act as displacements
        # from the position of the newly placed counter to check which surrounding counters to
        # switch from the opponent's colour to the current player's colour when they are outflanked
        valid_directions = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]

        directions_to_remove = []
        cells_to_flip = []

        for step in range(1,BOARD_SIZE):
            # Remove all direction vectors that were confirmed to not lead to valid
            # outflanked cells in the last iteration
            for d in directions_to_remove:
                valid_directions.remove(d)

            # Reset the list so that directions are not removed twice
            directions_to_remove.clear()

            for direction in valid_directions:
                # Get the change in position from the newly placed counter
                dx = direction[0]*step
                dy = direction[1]*step

                # Do not check the cell if the position to be searched is outside the board
                if 0 > x+dx or x+dx >= BOARD_SIZE or 0 > y+dy or y+dy >= BOARD_SIZE:
                    continue

                # Get the status of cell being checked
                check_cell = board[y + dy][x + dx]

                # An empty cell reached before reaching another counter of the same colour
                # means that there are no coutners outflanked in this direction
                if check_cell == "None ":
                    directions_to_remove.append(direction)

                # Checks if a counter of the same colour is reached
                elif check_cell == current_player_colour:
                    # Adds the positions of the cells in a line between the newly added counter
                    # and the discovered counter of the same colour (if any) to a list
                    # of positions of counters that have been outflanked
                    for i in range(1, step):
                        cells_to_flip.append((x+direction[0]*i,y+direction[1]*i))
                    directions_to_remove.append(direction)

        # Switch the colour of the counters in the cells that were
        # outflanked by the newly added counter
        for cell_coords in cells_to_flip:
            x = cell_coords[0]
            y = cell_coords[1]

            # Toggle the colour of the counter at that position
            board[y][x] = "Dark " if board[y][x] == "Light" else "Light"

        # Print the status of the board after the turn for the next player
        components.print_board(board)

        # Change the turn to the other player
        current_player_colour = "Dark " if current_player_colour == "Light" else "Light"

        # If the move counter is depleted then end the game
        if move_counter == 0:
            print("No more moves left. Game over!")
            game_won = True

    # Count final number of counters of each colour on the board
    dark_counters = 0
    light_counters = 0

    # Add up the total counters in every row for each colour
    for row in board:
        dark_counters += row.count("Dark ")
        light_counters += row.count("Light")

    # Decides who wins the game based on who has a higher number of total counters on the board
    # If both players have the same amount of counters then the game ends in a draw
    if dark_counters > light_counters:
        print(f"Dark wins the game with {dark_counters} total counters!")
        print(f"(Light had {light_counters} counters)")
    elif light_counters > dark_counters:
        print(f"Light wins the game with {light_counters} total counters!")
        print(f"(Dark had {dark_counters} counters)")
    else:
        print("The game ended in a draw!")

if __name__ == "__main__":
    simple_game_loop()
