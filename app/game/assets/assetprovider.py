"""
Module that contains the asset provider class
"""
from settings import Settings

from .chessspritesheet import ChessSpriteSheet
from .factory import PiecesFactory


class AssetsProvider:
    """
    A simple provider which is responsible for
    binding and propagating the currently used piece factory
    """
    def __init__(self) -> None:
        chess_sprite_sheet = ChessSpriteSheet(Settings().get_chess_assets_path())
        self._pieces_factory = PiecesFactory(chess_sprite_sheet)

    def get_pieces_factory(self) -> PiecesFactory:
        """Gets piece factory

        :return: An instance of PiecesFactory
        """
        return self._pieces_factory

    def replace_pieces_factory(self, pieces_factory: PiecesFactory) -> None:
        """Replaces a bound factory

        :param pieces_factory:
        """
        self._pieces_factory = pieces_factory
