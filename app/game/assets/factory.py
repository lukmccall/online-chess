"""
A module which contains a factory of pieces
"""
from typing import Tuple

from constants import Team

from .chessspritesheet import ChessSpriteSheet
from ..piceces import ChessPieceEnum, ChessPieceSprite


class PiecesFactory:  # pylint: disable=R0903
    """
    Class which construct a piece type with correct image from given spite sheet
    """
    def __init__(self, chess_sprite_sheet: ChessSpriteSheet) -> None:
        """

        :param chess_sprite_sheet: A chess piece sprite sheet
        which will be use to construct pieces
        """
        self._chess_sprite_sheet = chess_sprite_sheet

    def crete_piece(
            self,
            piece_type: ChessPieceEnum,
            team: Team,
            position: Tuple[int, int],
            cell_size: Tuple[int, int]
    ) -> ChessPieceSprite:
        """Create piece from provided arguments

        :param piece_type: Type of piece
        :param team: Team
        :param position: Position(row and col) of piece
        :param cell_size: Size of single board cell
        :return: A created ChessPieceSprite object
        """
        img = self._chess_sprite_sheet.get_piece_image(piece_type, team)
        return ChessPieceSprite(img, position, team, cell_size)
