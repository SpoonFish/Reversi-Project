import components

BOARD_SIZE = 8

def cli_input_coords():
    """
    Requests column and row number of the cell the player wants to place a counter on until valid numbers are inputted.

    Returns:
        tuple(int,int): The x and y position of the players desired move.
    """
    
    while True:
        x = input("Enter x coordinate of move: ")
        y = input("Enter y coordinate of move: ")
        if not x.isdecimal() or not y.isdecimal():
            print("Coordinates must both be whole numbers. Try again")
            continue
        x = int(x)
        y = int(y)
        if x < 1 or y < 1 or x > BOARD_SIZE or y > BOARD_SIZE:
            print(f"Coordinate numbers must be whole numbers within 0 and {BOARD_SIZE}")
            continue
        return (x, y)
    
def simple_game_loop():
    """
    Initialises the game, processes the players' moves and ends the game . 
    """
    
    print("Welcome to CLI Reversi! :)")

    board = components.initialise_board(BOARD_SIZE)

    move_counter = 60
    current_player_colour = "Dark "
    game_won = False
    components.print_board(board)
    previous_turn_passed = False

    while not game_won:
        has_legal_move = False
        for y, row in enumerate(board):
            for x, space in enumerate(row):
                if space != "None ":
                    continue
                if components.legal_move(current_player_colour, (x+1, y+1), board):
                    has_legal_move = True

        if not has_legal_move:
            current_player_colour = "Dark " if current_player_colour == "Light" else "Light"
            print(f"{current_player_colour.strip()} has no legal moves! Passing turn")
            if previous_turn_passed:
                print("No more legal moves can be made by either player. Game over!")
                game_won = True
            previous_turn_passed = True
            continue

        previous_turn_passed = False

        print(f"{move_counter} max moves left")
        print(f"Its {current_player_colour.strip()}'s turn")

        move = (0, 0)
        while True:
            move = cli_input_coords()
            if components.legal_move(current_player_colour, move, board):
                break
            print("Move is invalid. Try again")

        move_counter -= 1

        x = move[0] - 1
        y = move[1] - 1

        board[y][x] = current_player_colour
        opposite_colour = "Dark " if current_player_colour == "Light" else "Light"
        valid_directions = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
        directions_to_remove = []
        spaces_to_flip = []

        for step in range(1,BOARD_SIZE):
            for d in directions_to_remove:
                valid_directions.remove(d)

            if len(valid_directions) == 0:
                break

            directions_to_remove.clear()

            for direction in valid_directions:
                dx = direction[0]*step
                dy = direction[1]*step

                if 0 > x+dx or x+dx >= BOARD_SIZE or 0 > y+dy or y+dy >= BOARD_SIZE: 
                    continue

                check_space = board[y + dy][x + dx]

                if check_space == "None ":
                    directions_to_remove.append(direction)
                    
                elif check_space == current_player_colour:
                    for i in range(1, step):
                        spaces_to_flip.append((x+direction[0]*i,y+direction[1]*i))
                    directions_to_remove.append(direction)

        
        for space_coords in spaces_to_flip:
            x = space_coords[0]
            y = space_coords[1]
            board[y][x] = "Dark " if board[y][x] == "Light" else "Light"

        components.print_board(board)
        current_player_colour = "Dark " if current_player_colour == "Light" else "Light"

        if move_counter == 0:
            print("No more moves left. Game over!")
            game_won = True

    dark_counters = 0
    light_counters = 0
    for row in board:
        dark_counters += row.count("Dark ")
        light_counters += row.count("Light")

    if dark_counters > light_counters:
        print(f"Dark wins the game with {dark_counters} total counters! (Light had {light_counters} counters)")
    elif light_counters > dark_counters:
        print(f"Light wins the game with {light_counters} total counters! (Dark had {dark_counters} counters)")
    else:
        print("The game ended in a draw!")

if __name__ == "__main__":
    simple_game_loop()