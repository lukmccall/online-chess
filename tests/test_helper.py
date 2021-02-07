from unittest import TestCase
import types

import chess

from constants import Team
from game import ChessPieceEnum
from game.boards.helper import \
    iterate_over_board_squares,\
    map_piece_types,\
    map_piece_color,\
    map_square_to_index


class TestHelper(TestCase):

    def test_iterate_over_board_squares(self):
        it = iterate_over_board_squares()
        all_squares = list(it)

        self.assertIsInstance(it, types.GeneratorType)
        self.assertListEqual(all_squares, list(chess.SQUARES))

    def test_map_piece_types(self):
        self.assertEqual(map_piece_types(chess.KING), ChessPieceEnum.KING)
        self.assertEqual(map_piece_types(chess.BISHOP), ChessPieceEnum.BISHOP)
        self.assertEqual(map_piece_types(chess.PAWN), ChessPieceEnum.PAWN)

    def test_map_piece_color(self):
        self.assertEqual(map_piece_color(chess.WHITE), Team.WHITE)
        self.assertEqual(map_piece_color(chess.BLACK), Team.BLACK)

    def test_map_square_to_index(self):
        self.assertEqual(map_square_to_index(chess.A1), (0, 0))
        self.assertEqual(map_square_to_index(chess.D4), (3, 3))
        self.assertEqual(map_square_to_index(chess.H8), (7, 7))
        self.assertEqual(map_square_to_index(chess.E7), (6, 4))
