"""
A module that contains GameBoardInterface
"""
from typing import Optional, Iterator, List

from langextensions import Interface, abstract

import chess

from ..piceces import ChessPieceSprite


class GameBoardInterface(metaclass=Interface):
    """
    Interface of graphic and logic game board
    """
    @abstract
    def get_possible_moves_from(self, row: int, col: int) -> Iterator[chess.Move]:
        """Gets possible moves from given square

        :param row: Row
        :param col: Col
        :return: A iterator of all possible moves
        """

    @abstract
    def generate_move(
            self,
            from_row: int,
            from_col: int,
            to_row: int,
            to_col: int
    ) -> Optional[chess.Move]:
        """Generates move between tow squares

        :param from_row: Row of source square
        :param from_col: Col of source square
        :param to_row: Row of target square
        :param to_col: Col of target square
        :return: Move if exists otherwise None
        """

    @abstract
    def draw(self) -> None:
        """Draws board
        """

    @abstract
    def draw_moves(self, moves: List[chess.Move]) -> None:
        """Draws moves from provided list

        :param moves: List of moves
        """

    @abstract
    def is_game_over(self) -> bool:
        """Checks if the game is over

        :return: True if game was finished otherwise False
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

    @abstract
    def set_flip(self, new_value: bool) -> None:
        """Controls the "flip" behaviour of the board

        :param new_value: whatever the board should be flipped
        """

    @abstract
    def move(self, move: chess.Move) -> None:
        """Executes provided move

        :param move: Move
        :raise AssertionError: if the move is illegal
        """

    @abstract
    def get_piece_at(self, row: int, col: int) -> Optional[ChessPieceSprite]:
        """Gets a piece at given square

        :param row: Row of square
        :param col: Col of square
        :return: ChessPieceSprite if the piece exists on the provided square
        otherwise returns None
        """
