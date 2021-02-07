from unittest import TestCase, mock
import chess

from game import PythonChessLogicBoard


class TestPythonChessLogicBoard(TestCase):
    @mock.patch("chess.Board.result", return_value="1/2-1/2")
    @mock.patch("chess.Board.is_game_over", return_value=True)
    def test_winner_draw(self, mocked_chess_board_is_game_over, mocked_chess_board_result):
        board = PythonChessLogicBoard()

        winner = board.winner()

        mocked_chess_board_is_game_over.assert_called_once()
        mocked_chess_board_result.assert_called_once()
        self.assertEqual(winner, None)

    @mock.patch("chess.Board.result", return_value="1-0")
    @mock.patch("chess.Board.is_game_over", return_value=True)
    def test_winner_white(self, mocked_chess_board_is_game_over, mocked_chess_board_result):
        board = PythonChessLogicBoard()

        winner = board.winner()

        mocked_chess_board_is_game_over.assert_called_once()
        mocked_chess_board_result.assert_called_once()
        self.assertEqual(winner, chess.WHITE)

    @mock.patch("chess.Board.result", return_value="0-1")
    @mock.patch("chess.Board.is_game_over", return_value=True)
    def test_winner_white(self, mocked_chess_board_is_game_over, mocked_chess_board_result):
        board = PythonChessLogicBoard()

        winner = board.winner()

        mocked_chess_board_is_game_over.assert_called_once()
        mocked_chess_board_result.assert_called_once()
        self.assertEqual(winner, chess.BLACK)

    @mock.patch("chess.Board.result", return_value="0-1")
    @mock.patch("chess.Board.is_game_over", return_value=False)
    def test_winner_none_if_game_is_not_over(self, mocked_chess_board_is_game_over, mocked_chess_board_result):
        board = PythonChessLogicBoard()

        winner = board.winner()

        mocked_chess_board_is_game_over.assert_called()
        self.assertFalse(mocked_chess_board_result.call_args_list)
        self.assertEqual(winner, None)
