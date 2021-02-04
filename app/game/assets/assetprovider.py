from settings import Settings

from .chessspritesheet import ChessSpriteSheet
from .factory import PiecesFactory


class AssetsProvider:
    def __init__(self):
        chess_sprite_sheet = ChessSpriteSheet(Settings().get_chess_assets_path())
        self.pieces_factory = PiecesFactory(chess_sprite_sheet)

    def get_pieces_factory(self) -> PiecesFactory:
        return self.pieces_factory

    def replace_pieces_factory(self, pieces_factory: PiecesFactory):
        self.pieces_factory = pieces_factory
