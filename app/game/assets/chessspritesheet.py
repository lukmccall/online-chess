"""
A module that contains a chess sprite sheet
"""
from typing import ValuesView, Dict, Tuple
import pygame

from constants import Team

from .spritesheet import SpriteSheet
from ..piceces import ChessPieceEnum


class ChessSpriteSheet:
    """
    Class which is encapsulate a functionality connect witch chess sprite sheet
    This sprite sheet has a special form which indicates arrangement of the pieces
    """
    def __init__(self, filename: str) -> None:
        """
        :param filename: A path to the "chess" sprite sheet
        """
        sprite_sheet = SpriteSheet(filename)
        images = sprite_sheet.images(2, 6)

        piece_num = 0
        self._pieces_type_image: Dict[Tuple[ChessPieceEnum, Team], pygame.surface.Surface] = {}

        for team in (Team.WHITE, Team.BLACK):
            for piece_type in (
                    ChessPieceEnum.KING,
                    ChessPieceEnum.QUEEN,
                    ChessPieceEnum.BISHOP,
                    ChessPieceEnum.KNIGHT,
                    ChessPieceEnum.ROOK,
                    ChessPieceEnum.PAWN):
                self._pieces_type_image[(piece_type, team)] = images[piece_num]
                piece_num += 1

    def get_piece_image(self, piece_type: ChessPieceEnum, team: Team) -> pygame.surface.Surface:
        """Gets a piece image

        :param piece_type: Type of the piece
        :param team: Piece team
        :return: A surface containing piece image
        """
        return self._pieces_type_image[(piece_type, team)]

    def get_all_images(self) -> ValuesView[pygame.surface.Surface]:
        """Gets all images

        :return: An collection of all images in the sprite sheet
        """
        return self._pieces_type_image.values()
