"""
Tests for components.py
"""

import unittest
import io
import contextlib
import components

class TestInitialiseBoard(unittest.TestCase):
    """
    Contains tests for the function initialise_board
    """

    def test_board_is_correct_size(self):
        """
        Test initialise_board creates a board of the correct specified sizes
        """

        # Test different sizes of boards
        board = components.initialise_board(8)
        self.assertEqual(len(board), 8)
        self.assertTrue(all(len(row) == 8 for row in board))

        board = components.initialise_board(10)
        self.assertEqual(len(board), 10)
        self.assertTrue(all(len(row) == 10 for row in board))

        board = components.initialise_board(16)
        self.assertEqual(len(board), 16)
        self.assertTrue(all(len(row) == 16 for row in board))

        board = components.initialise_board(4)
        self.assertEqual(len(board), 4)
        self.assertTrue(all(len(row) == 4 for row in board))

    def test_board_cells_initialised_as_none(self):
        """
        Test initialise_board creates the board filled with empty cells except the middle 4 cells
        """

        board = components.initialise_board(8)
        # Only 4 centre squares should not be "None "
        non_none_positions = [
            (len(board)//2, len(board)//2),
            (len(board)//2 - 1, len(board)//2 - 1),
            (len(board)//2 - 1, len(board)//2),
            (len(board)//2, len(board)//2 - 1)
        ]

        for y in range(8):
            for x in range(8):
                if (y, x) in non_none_positions:
                    continue
                self.assertEqual(board[y][x], "None ")

    def test_starting_pieces_correct(self):
        """
        Test initialise_board creates the correct alternating pattern in the
        middle 4 squares of the board
        """

        # Check pattern of counters in the middle is correct
        board = components.initialise_board(8)

        mid = 8 // 2

        # Assert the exact positions of the starting counters ensuring they are the correct colours
        self.assertEqual(board[mid][mid], "Dark ")
        self.assertEqual(board[mid - 1][mid - 1], "Dark ")
        self.assertEqual(board[mid - 1][mid], "Light")
        self.assertEqual(board[mid][mid - 1], "Light")

    # Check different invalid inputs for initialise_board
    def test_invalid_size_type(self):
        """
        Test initialise_board does not accept data of an invalid type
        """

        with self.assertRaises(TypeError):
            components.initialise_board("8")

    def test_invalid_size_odd(self):
        """
        Test initialise_board does nto accept odd numbers
        """

        with self.assertRaises(ValueError):
            components.initialise_board(5)

    def test_invalid_size_too_small(self):
        """
        Test initialise_board does not accept sizes too small
        """

        with self.assertRaises(ValueError):
            components.initialise_board(2)

    def test_invalid_size_too_large(self):
        """
        Test initialise_board does not accept sizes too large
        """

        with self.assertRaises(ValueError):
            components.initialise_board(20)


class TestLegalMove(unittest.TestCase):
    """
    Contains tests for the function legal_move
    """

    def setUp(self):
        """
        Generate an initial board to check legal moves on for each test
        """

        # Set up a default board fro the tests
        self.board = components.initialise_board(8)

    def test_initial_legal_moves_for_dark(self):
        """
        Test legal_move correctly identifies the 4 possible starting moves for Dark as legal
        """

        # Standard initial legal moves in Reversi for the dark player
        legal_moves = [(4, 6), (3, 5), (5, 3), (6, 4)]
        for move in legal_moves:
            with self.subTest(move=move):
                self.assertTrue(components.legal_move("Dark ", move, self.board))

    def test_initial_illegal_moves(self):
        """
        Test legal_move correctly identifies these other moves as illegal at the start of the game
        """

        # Corners are illegal at game start
        illegal_moves = [(1, 1), (8, 8), (1, 8), (8, 1)]
        for move in illegal_moves:
            with self.subTest(move=move):
                self.assertFalse(components.legal_move("Dark ", move, self.board))

    def test_move_on_occupied_square(self):
        """
        Test legal_move correctly identifies the middle cells as invalid moves as they are occupied
        """

        # Center cells are occupied
        self.assertFalse(components.legal_move("Dark ", (4, 4), self.board))
        self.assertFalse(components.legal_move("Light", (5, 5), self.board))

    def test_move_out_of_bounds_does_not_crash(self):
        """
        Test legal_move does not crash and returns False for moves out of range
        """

        self.assertFalse(components.legal_move("Dark ", (-1, 2), self.board))

    def test_valid_flanking_move(self):
        """
        Test legal_move works in a scenario where there is a valid move that outflanks a counter
        """

        # Create a scenario where a flanking move is legal away from center
        board = [["None " for _ in range(8)] for _ in range(8)]
        # Dark counter at (4, 4)
        board[3][3] = "Dark "
        # Light counter at (5, 4)
        board[3][4] = "Light"

        # Dark plays at (6, 4) which flanks Light at (5, 4)
        self.assertTrue(components.legal_move("Dark ", (6, 4), board))

class TestPrintBoard(unittest.TestCase):
    """
    Contains tests for the function print_board
    """

    def setUp(self):
        """
        Resets the board before the test
        """

        self.board = components.initialise_board(8)

    def test_print_board_output(self):
        """
        Test print_board outputs the correct ASCII representation        
        """

        # Capture the output of print_board using contextlib and io
        f = io.StringIO()
        with contextlib.redirect_stdout(f):
            components.print_board(self.board)

        # Store the output as a string
        output = f.getvalue()

        # Check that expected phrases are in the ouput
        self.assertIn("1", output)
        self.assertIn("Dark", output)
        self.assertIn("Light", output)
        self.assertIn("None", output)

if __name__ == "__main__":
    unittest.main()
