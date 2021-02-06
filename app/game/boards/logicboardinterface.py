"""
A module that contains LogicBoardInterface
"""
from typing import Optional, Iterator

import chess

from langextensions import Interface, abstract


class LogicBoardInterface(metaclass=Interface):
    """Interface of the logic board
    """
    @abstract
    def get_possible_moves_from(self, row: int, col: int) -> Iterator[chess.Move]:
        """Gets possible moves from given square

        :param row: Row
        :param col: Col
        :return: A iterator of all possible moves
        """

    @abstract
    def execute_move(self, move: chess.Move) -> None:
        """Executes provided move

        :param move: Move
        """

    @abstract
    def get_generate_move_from_to(
            self,
            from_square_row: int,
            from_square_col: int,
            to_square_row: int,
            to_square_col: int
    ) -> Optional[chess.Move]:
        """Gets all move between two squares

        :param from_square_row: Row of source square
        :param from_square_col: Col of source square
        :param to_square_row: Row of target square
        :param to_square_col: Col of target square
        :return: Move if exists otherwise None
        """

    @abstract
    def is_game_over(self) -> bool:
        """Checks if the game is over

        :return: True if game was finished otherwise False
        """

    @abstract
    def is_move_legal(self, move: chess.Move) -> bool:
        """Checks if the move is legal

        :param move: Move to check
        :return: whatever the move is legal or not
        """

    @abstract
    def is_en_passant(self, move: chess.Move) -> bool:
        """Checks if the move is "en passant"

        :param move: Move to check
        :return: whatever the move is en passant or not
        """

    @abstract
    def is_castling(self, move: chess.Move) -> bool:
        """Checks if the move is castling

        :param move: Move to check
        :return: whatever the move is castling or not
        """

    @abstract
    def piece_at(self, square: chess.Square) -> Optional[chess.Piece]:
        """Returns piece at given square

        :param square: Square
        :returns Piece if exists otherwise None
        """

    @abstract
    def turn(self) -> chess.Color:
        """Gets current team

        :return: Currently playing team
        """

    @abstract
    def winner(self) -> Optional[chess.Color]:
        """Gets winner

        :return: Winner team or None if draw
        """
