from typing import ValuesView
import pygame

from constants import Team

from .spritesheet import SpriteSheet
from ..piceces import ChessPieceEnum


class ChessSpriteSheet:
    def __init__(self, filename: str):
        sprite_sheet = SpriteSheet(filename)
        images = sprite_sheet.images(2, 6)

        piece_num = 0
        self.pieces_type_image = {}

        for team in (Team.WHITE, Team.BLACK):
            for piece_type in (
                    ChessPieceEnum.KING,
                    ChessPieceEnum.QUEEN,
                    ChessPieceEnum.BISHOP,
                    ChessPieceEnum.KNIGHT,
                    ChessPieceEnum.ROOK,
                    ChessPieceEnum.PAWN):
                self.pieces_type_image[(piece_type, team)] = images[piece_num]
                piece_num += 1

    def get_piece_image(self, piece_type: ChessPieceEnum, team: Team) -> pygame.Surface:
        return self.pieces_type_image[(piece_type, team)]

    def get_all_images(self) -> ValuesView[pygame.surface.Surface]:
        return self.pieces_type_image.values()
