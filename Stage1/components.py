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

def legal_move(colour,coord,board):
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