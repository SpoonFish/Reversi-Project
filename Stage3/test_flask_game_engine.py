"""
Tests for flask_game_engine.py
"""

import io
import json
import unittest
import flask_game_engine as fge


class TestGameFunctions(unittest.TestCase):
    """
    Contains tests for the game logic functions
    """

    def setUp(self):
        """
        Set up the initial game conditions for the tests
        """

        # Reset the game state before each test
        fge.game_state['board'] = fge.components.initialise_board()
        fge.game_state['current_player'] = 'Dark '
        fge.game_state['game_won'] = False

    def test_execute_move_flips(self):
        """
        Test that execute_move correctly flips outflanked counters
        """

        board = fge.components.initialise_board()
        board = fge.execute_move('Dark ', (4, 3), board)
        # Counter placed at (4,3)
        self.assertEqual(board[2][3], 'Dark ')
        # Check that a counter is flipped (initial position (4,4) is Dark so (4,4) remains Dark)
        self.assertEqual(board[3][3], 'Dark ')

    def test_pass_turn(self):
        """
        Test that pass_turn changes the turn in the game state to the other player
        """

        fge.game_state['current_player'] = 'Dark '
        fge.pass_turn()
        self.assertEqual(fge.game_state['current_player'], 'Light')
        fge.pass_turn()
        self.assertEqual(fge.game_state['current_player'], 'Dark ')

    def test_calculate_winner_dark_wins(self):
        """
        Test calculate_winner returns the correct winner (Dark)
        when most counters on the board are dark
        """

        # Fill board so Dark has more
        for y in range(8):
            for x in range(8):
                fge.game_state['board'][y][x] = 'Dark '
        # Add one Light counter
        fge.game_state['board'][0][0] = 'Light'
        self.assertEqual(fge.calculate_winner(), 'dark')

    def test_calculate_winner_draw(self):
        """
        Test calculate_winner returns 'draw' when number of light and dark coutners
        is equal
        """

        # Initial board has 2 counters of each colour so it is ideal for this test
        board = fge.components.initialise_board()
        fge.game_state['board'] = board
        self.assertEqual(fge.calculate_winner(), 'draw')

    def test_legal_move_available_true(self):
        """
        Test legal_move_available identifies that there are moves available
        at the start of the game
        """

        # Initial state of the game should have legal moves available
        board = fge.components.initialise_board()
        self.assertTrue(fge.legal_move_available('Dark ', board))

    def test_legal_move_available_false(self):
        """
        Test legal_move_available identifies that there are no moves available
        if the board is full
        """

        # Fill board completely with Dark so no moves should be available
        board = [['Dark ' for _ in range(8)] for _ in range(8)]
        self.assertFalse(fge.legal_move_available('Light', board))

class FlaskGameEngineTests(unittest.TestCase):
    """
    Contains tests for the Flask routes for the web applciation
    """

    # App only needsto be set up once
    @classmethod
    def setUpClass(cls):
        """
        Initially set up the Flask app as a test client for the tests
        """

        fge.app.config['TESTING'] = True

        # test_client() from Flask helps to test the Flask related parts
        cls.client = fge.app.test_client()

    # Some tests change the board so this method runs before each test
    def setUp(self):
        """
        Reset the board, turn and if the game is won or not for each test
        """

        # Reset game state before each test
        fge.game_state['board'] = fge.components.initialise_board()
        fge.game_state['current_player'] = 'Dark '
        fge.game_state['game_won'] = False

    def test_index_route(self):
        """
        Test to check if the main page loads correctly
        """

        response = self.client.get('/')

        # status code 200 means the request was succesfully processed by the server
        self.assertEqual(response.status_code, 200)

        # Check the beginning of the HTML tag is anywhere in the response data as bytes
        self.assertIn(b'<html', response.data)

    def test_save_game_route(self):
        """
        Test saving the game provides the correct format of data in a JSON file
        """

        response = self.client.get('/save')
        self.assertEqual(response.status_code, 200)
        # Check the type of data is JSON
        self.assertEqual(response.mimetype, 'application/json')
        data = json.loads(response.data)
        self.assertIn('board', data)
        self.assertIn('current_player', data)
        self.assertIn('game_won', data)

    def test_load_game_route(self):
        """
        Test loading the game from a file works correctly
        """

        # Create example save file data
        save_data = {
            "board": fge.components.initialise_board(),
            "current_player": "Dark ",
            "game_won": False
        }
        # Comvert to JSON
        file_data = io.BytesIO(json.dumps(save_data).encode())
        file_data.name = 'reversi_save.json'

        response = self.client.post('/load', data={'file': file_data}, content_type='multipart/form-data')
        # Should redirect to index
        self.assertEqual(response.status_code, 302)
        self.assertEqual(fge.game_state['current_player'], 'Dark ')

    def test_reset_game_route(self):
        """
        Test resetting the game returns game_state to its original state
        """

        # Create random differences from initial game data to see if it gets reset
        fge.game_state['current_player'] = 'Light'
        fge.game_state['game_won'] = True
        self.client.post('/reset')

        # Check the values are reset
        self.assertEqual(fge.game_state['current_player'], 'Dark ')
        self.assertFalse(fge.game_state['game_won'])
        self.assertEqual(len(fge.game_state['board']), 8)
        self.assertEqual(fge.game_state['board'][3][3], "Dark ")

    def test_ai_move_route(self):
        """
        Test that the AI returns a valid move
        """

        response = self.client.get('/ai_move')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'success')

        # Check the move calculated is not out of range
        self.assertTrue(1 <= data['x'] <= 8)
        self.assertTrue(1 <= data['y'] <= 8)

    def test_move_route_valid(self):
        """
        Test that making a legal move passes the turn
        """

        # This move should be valid for dark on the first turn
        response = self.client.get('/move', query_string={'x': 4, 'y': 6})
        data = json.loads(response.data)

        # Check the turn is passed and that it was a legal move
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['player'], 'Light')
        self.assertEqual(len(data['board']), 8)

    def test_move_route_invalid(self):
        """
        Test an invalid move returns a fail status and a message saying the move is not legal
        """

        # Board initially has Dark counter at (4,4) so this move should be invalid
        response = self.client.get('/move', query_string={'x': 4, 'y': 4})
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'fail')
        self.assertIn('Move is not legal', data['message'])


if __name__ == '__main__':
    unittest.main()
