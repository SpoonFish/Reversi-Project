"""
Flask Web Application implementation of Reversi 

Implements a web-based Reversi game using Flask. There is functionality
for playing the game, resetting the game and saving and loading games as
JSON files. Game logic and board management are handled via helper
functions and the 'components' module.
"""

import json
import io
import flask
import components

app = flask.Flask(__name__)

# Initialise the board,keep track of whos turn it is,
# and store if the game is won values in a dictionary
# so the values can be changed during the move() function
game_state = {
    "board": components.initialise_board(8),
    "current_player": "Dark ",
    "game_won": False
}

def execute_move(colour,coord,board):
    """
    Updates the board after a player places a counter at the given coordinates.
    Flips outflanked opponent counters according to the standard rules of Reversi.

    Parameters:
        colour (str): The colour of the counters of the player making the move
        coord (list[int,int]): Contains the coordinates where the player wants to place their counter
        board (list[list[str]]): The board containing the state of the game that will be updated


    Returns:
        list[list[str]]: The updated state of the board
    """

    # Convert to list indices
    x = coord[0] - 1
    y = coord[1] - 1

    # Set the cell selected by the player to a counter of their colour
    board[y][x] = colour

    # Stores a set of directions vectors which will act as displacements
    # from the position of the newly placed counter to check which surrounding counters to
    # switch from the opponent's colour to the current player's colour when they are outflanked
    valid_directions = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]

    directions_to_remove = []
    cells_to_flip = []

    for step in range(1,8):
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
            if 0 > x+dx or x+dx >= 8 or 0 > y+dy or y+dy >= 8:
                continue

            # Get the status of cell being checked
            check_cell = board[y + dy][x + dx]

            # An empty cell reached before reaching another counter of the same colour
            # means that there are no coutners outflanked in this direction
            if check_cell == "None ":
                directions_to_remove.append(direction)

            # Checks if a counter of the same colour is reached
            elif check_cell == colour:
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

    return board

def pass_turn():
    """
    Changes the current player's turn to the other colour.
    """
    # Toggles player
    game_state["current_player"] = "Dark " if game_state["current_player"] == "Light" else "Light"

def calculate_winner():
    """
    Checks which player has more counters at the end of the game or if the game ended in a draw.

    Returns:
        str: The colour that has the most counters of that colour on the board or 'draw' if it is equal
    """
    dark_total = 0
    light_total = 0

    # Add total number of each player's counters in each row
    for row in game_state["board"]:
        dark_total += row.count("Dark ")
        light_total += row.count("Light")

    # Determines who wins depending on who got more counters
    if dark_total > light_total:
        return "dark"
    elif light_total > dark_total:
        return "light"
    else:
        return "draw"

def legal_move_available(colour, board):
    """
    Check if the player can make a legal move on this turn

    Parameters:
        colour (str): The player being checked for legal moves
        board (list[list[str]]): The board containing the state of the game

    Returns:
        bool: True if there is a move available, False if not
    """
    # Check there is a legal move for the current player
    for y, row in enumerate(board):
        for x, cell in enumerate(row):
            if cell != "None ":
                continue

            # If there is at least one legal move to make, return True
            if components.legal_move(colour, (x+1, y+1), board):
                return True
    return False

@app.route("/")
def index():
    """
    Renders the main page for the game including the board, game log and buttons
    """

    # Sends the state of the board and the current player
    # so they can be used when loading the webpage
    return flask.render_template("index.html", game_board=game_state["board"], turn=game_state["current_player"].strip())

@app.route('/save', methods=['GET'])
def save_game():
    """
    Downloads the state of the current game as a json file to the user's device
    """

    # Game_state is a dictionary so it can be easily converted to json
    json_str = json.dumps(game_state, indent=4)
    buffer = io.BytesIO()
    buffer.write(json_str.encode())
    buffer.seek(0)
    return flask.send_file(buffer, as_attachment=True, download_name="reversi_save.json", mimetype='application/json')

@app.route('/load', methods=['POST'])
def load_game():
    """
    Loads a game from a state saved in the uploaded json file
    """

    # Check if there is a file to load
    if 'file' not in flask.request.files:
        return "No file uploaded", 400
    
    # Get the file from the request
    file = flask.request.files['file']
    
    # Check file name is not empty
    if file.filename == '':
        return "No selected file", 400
    try:
        # Load values from the file json to game_state
        loaded_game_state = json.load(file)
        game_state["board"] = loaded_game_state["board"]
        game_state["game_won"] = loaded_game_state["game_won"]
        game_state["current_player"] = loaded_game_state["current_player"]
        return flask.redirect(flask.url_for('index'))
    
    # Return an error with error information if the loading of values to game_state fails
    except Exception as e:
        return f"Error loading file: {e}", 400

@app.route('/reset', methods=['POST'])
def reset_game():
    """
    Reset the current game so players can start a new game
    """
    
    # Set values in game_state to their initial values and reload the page
    game_state["board"] = components.initialise_board(8)
    game_state["game_won"] = False
    game_state["current_player"] = "Dark "
    return flask.redirect(flask.url_for('index'))

@app.route("/move")
def move():
    """
    Handles turn passing, updating the board and game log when the player attempts to make a move
    """

    # Check if the game is still playable
    if game_state["game_won"]:
        return flask.jsonify(status="fail", message="The game is over")

    # Get x and y from the GET request
    # If a coordinate is not numeric, it is set to None
    x = flask.request.args.get("x", type=int)
    y = flask.request.args.get("y", type=int)

    # Check coordinates are not None and that they are on the board
    if x is None or y is None or x < 1 or y < 1 or x > 8 or y > 8:
        return flask.jsonify(status="fail", message=f"Coordinates must be whole number between 1 and {8}")

    # Check if move is legal for the current player
    if components.legal_move(game_state["current_player"], (x, y), game_state["board"]):
        # Place new counter and flip outflanked counters
        game_state["board"] = execute_move(game_state["current_player"], (x, y), game_state["board"])

        pass_turn()

        # Skip the players turn if they have no available legal moves
        if not legal_move_available(game_state["current_player"], game_state["board"]):
            pass_turn()
            # If the next player also cant make a move then the game is over
            if not legal_move_available(game_state["current_player"], game_state["board"]):
                winner = calculate_winner()
                game_state["game_won"] = True

                # Return a response indicating the game ended with a message of who won
                if winner == "draw":
                    return flask.jsonify(status="success", finished="Neither player can make a legal move! The game is over. The game ended in a draw", player=game_state["current_player"], board=game_state["board"])
                else:
                    return flask.jsonify(status="success", finished=f"Neither player can make a legal move! The game is over. The player with {winner} counters won!", player=game_state["current_player"], board=game_state["board"])
            return flask.jsonify(status="success", player=game_state["current_player"], board=game_state["board"], message=f"No legal moves available for {"Light" if game_state["current_player"] == "Dark " else "Dark "}. Turn was passed")

        # A valid completed move returns a success with the updated board to be displayed
        return flask.jsonify(status="success", player=game_state["current_player"], board=game_state["board"])

    else:
        # An invalid move returns a fail
        return flask.jsonify(status="fail", message="Move is not legal")

if __name__ == "__main__":
    app.run()
