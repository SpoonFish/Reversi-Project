# Reversi Web Application
## Overview
This project is a web version of the board game Reversi otherwise known as Othello. The project uses Flask for the backend and HTML CSS JS for the frontend.
In this application players are able to play Reversi against another player on the same device or play against an AI. The game log shows who's turn it is, what moves have been made, whether a move is valid or not and who wins the game. There are also buttons to save and load the game from a file and reset the current game.

The backend handles the processing of moves, save file generation, AI move calculation, turn switching and game ending conditions.

The AI algorithm used in the project focuses on strategic, positional gameplay. It uses a score map that assigns a score to each cell on the board. The higher the score, the more positonally advantageous the move at that position likely is. This gives the AI a good sense of corner control as corners are valuable positions to claim in Reversi because they cannot be outflanked. The AI will play the first legal move with the highest score it finds from the top left of the board along each row.

Instruction for use of the project are in 'MANUAL.pdf'

## Design breakdown and module reasoning
### `components.py`
Contains utility functions that carry out some of the core behaviours of the processing of moves in the game. There is no Flask code in this module making it usable for other implementations of Reversi.

Functions:
- `initialise_board(size=8)`
  - Purpose: Creates a board of width and height 'size' where size must be an even integer between 4 and 16. Fills each cell with the value "None " to indicate an empty space on the board. Places the 4 starting counters at the center of the board
  - Why this design?: Isolates board generation in a function away from main game code to keep logic modular.
 
- `print_board(board)`
  - Purpose: Prints an ASCII representation of the board provided to the console with coordinate axis.
  - Why this design?: Helps to debug the game code efficiently and can also be used as a way to play the game in the console directly.
 
- `legal_move(colour, coord, board)`
  - Purpose: Checks if a move is allowed to be played by checking it against the rules of Reversi using the current players turn, the coordinates of the desired move and the current state of the board. Uses vector based directional scanning.
  - Why this design?: Using directional scanning from the desired move coordinate allows scalable and efficient checking of legal moves for any board size. Separates logic of the game from the Flask related parts. Simply returns True if the move is legal and False if not.

### `flask_game_engine.py`
This module handles requests made by the web page so that moves can be made on the web page and the backend updates the board and renders the result of that move. Saving, loading and resetting of games is handled here. Also contains additional helper functions to process logic of the game that was not mentioned in the specification for `components.py` such as passing turns, placing counters and flipping outflanked counters for legal moves, and determining the winner of the game based on the end state of the board.

Key Variables:
- `game_state`
  - Purpose: Dictionary that holds global information about the game such as the board and its current state (where each counter is and what type they are), whos turn it currently is in the game and whether the game has been won or not.
  - Why this design?: Storing this information in one global dictionary removes the need to use the `global` keywork in functions requiring the game state data because the values within the dictionary are being changed, not the actual dictionary itself. It also makes saving and loading of the game state convenient as the dictionary can easily be converted and reccovered from a .json file.

- `ai_score_map`
  - Puprose: Contains the score values assigned to each cell of the board (web version only functions on 8x8 board). Scores above 0 are considered to be good moves, scores below 0 are considered bad moves. Move scores are measured by how positionally advantageous the move is for the AI player. For example, corner cells are the highest score moves the AI can make because the corner cannot be flipped once it is claimed providing a useful positional advantage.
  - Why this design?: The score map is stored globally because it is constant and does not change mid-game.

Functions:
- `execute_move(colour, coord, board)`
  - Purpose: Places a new counter at the location of the move being executed. Flips all counters that are outflanked by the move to the colour of the player who made the move.
  - Why this design?: Keeps the processing of moves modular so that the same code is used for either colour of player and for both human and AI players.

- `pass_turn()`
  - Purpose: Changes whos turn it is to the other player.
  - Why this design?: Keeps code readable and avoids repeating code as changing turns happens in multiple parts of the game.

- `calculate_winner()`
  - Purpose: Determines who won the game based on the final state of the board by counting how many counters of each colour there is. The player with the highest amount of their colour counters on the board wins. Also accounts for draws.
  - Why this design?: Allows the code to calculate the winner to be separate from the code that displays the winner. Can also be used easily in other implementations.

- `legal_move_available(colour, board)`
  - Purpose: Checks if there is an available move for the specified player on the board. This is used to make sure a player can actually make a move before asking them to. If they cannot then their turn is automatically passed.
  - Why this design?: This is useful for multiple applications in the game and enforcing the rule of Reversi where if a player cannot make a move the their move is passed. And if both players cannot make a move then the game is ended.

Flask App Routes:
- `/` (index page)
  - Purpose: Renders the main web page including the board, game log and additional buttons for saving, loading and resetting.
  - Why this design?: Having everything in one page makes the application simple and easy to navigate and use as there are not many features so multiple pages are not needed.

- `/move` (GET)
  - Purpose: Handles turn passing, updating the board and game log when the player attempts to make a move. Returns JSON data to update the render of the board and gamelog messages.
  - Why this design?: Allows the webpage to fetch required information to display the result of a move in the game.

- `/ai_move` (GET)
  - Purpose: Calculates the best move for the AI according to the score map by getting the legal move with the highest score available. Returns the coordinates of the best move to be used with /move.
  - Why this design?: Allows the calculation of the AI move to be done on the backend while being triggerable from the web page.
    
- `/save` (GET)
  - Purpose: Downloads the current state of the game as a .json file to the user's device. This is activated by a 'save game' button on the web page.
  - Why this design?: Allows the game to be easily saved in case the user wants to preserve a game in progress and continue it later or save the end result. Storing as files on the user's device is easy and allows multiple games to be saved with no risk to the server itself.

- `/load` (POST)
  - Purpose: Loads a game from the file uploaded to the web page on the form. Activated by a 'load game' button on the web page.
  - Why this design?: JSON files are easily serialisable and readable by humans and works with python dictionaries.

- `/reset` (POST)
  - Purpose: Resets the current game to the initial state. Activated by a 'reset game' button on the web page.
  - Why this design?: Allowing the game to be reset lets player play the game again after ending a game and also lets them reset the game if they no longer wish to continue with a game.

## Project Information

**Project Name:** Reversi Project<br>
**Author:** Matthew Risso<br>
**Created:** December 2025<br>
**Last Updated:** December 2025

## License
This project is licensed under the MIT License.  
See the `LICENSE` file included in the repository for details.


## Handle/Repository
The source code for this project is available at:
https://github.com/SpoonFish/Reversi-Project

## Flow Diagrams
![](https://github.com/SpoonFish/Reversi-Project/blob/main/Stage3/flowcharts/flowchart_ai_move.png)
![](https://github.com/SpoonFish/Reversi-Project/blob/main/Stage3/flowcharts/flowchart_calculate_winner.png)
![](https://github.com/SpoonFish/Reversi-Project/blob/main/Stage3/flowcharts/flowchart_print_board.png)
![](https://github.com/SpoonFish/Reversi-Project/blob/main/Stage3/flowcharts/flowchart_pass_turn.png)
![](https://github.com/SpoonFish/Reversi-Project/blob/main/Stage3/flowcharts/flowchart_legal_move.png)
![](https://github.com/SpoonFish/Reversi-Project/blob/main/Stage3/flowcharts/flowchart_legal_move_available.png)
![](https://github.com/SpoonFish/Reversi-Project/blob/main/Stage3/flowcharts/flowchart_execute_move.png)
![](https://github.com/SpoonFish/Reversi-Project/blob/main/Stage3/flowcharts/flowchart_initialise_board.png)
