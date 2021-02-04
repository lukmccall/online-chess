from typing import Tuple

from constants import Team

from .chessspritesheet import ChessSpriteSheet
from ..piceces import ChessPieceEnum, ChessPieceSprite


class PiecesFactory: # pylint: disable=R0903
    def __init__(self, chess_sprite_sheet: ChessSpriteSheet):
        self.chess_sprite_sheet = chess_sprite_sheet

    def crete_piece(
            self,
            piece_type: ChessPieceEnum,
            team: Team,
            position,
            cell_size: Tuple[int, int]
    ) -> ChessPieceSprite:
        img = self.chess_sprite_sheet.get_piece_image(piece_type, team)
        return ChessPieceSprite(img, position, team, cell_size)
