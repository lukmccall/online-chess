from typing import Tuple

import pygame

from piceces import Team, ChessPieceEnum, ChessPiece
from settings import Settings


class SpriteSheet:
    def __init__(self, filename):
        self.img = pygame.image.load(filename)

    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert_alpha()
        image.blit(self.img, (0, 0), rect)
        return image

    def images(self, rows, cols):
        height = self.img.get_height() // rows
        width = self.img.get_width() // cols
        result = []
        for row in range(rows):
            for col in range(cols):
                top_x = col * width
                top_y = row * height

                result.append(self.image_at((top_x, top_y, width, height)))

        return result


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


class PiecesFactory:
    def __init__(self, chess_sprite_sheet: ChessSpriteSheet):
        self.chess_sprite_sheet = chess_sprite_sheet

    def crete_piece(self, piece_type: ChessPieceEnum, team: Team, position, cell_size: Tuple[int, int]) -> ChessPiece:
        img = self.chess_sprite_sheet.get_piece_image(piece_type, team)
        return piece_type.get_class(img, position, team, cell_size)


class AssetsProvider:
    def __init__(self):
        chess_sprite_sheet = ChessSpriteSheet(Settings().get_chess_assets_path())
        self.pieces_factory = PiecesFactory(chess_sprite_sheet)

    def get_pieces_factory(self):
        return self.pieces_factory
