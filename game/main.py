import sys
import os

from engine import GameManager
from settings import Settings
from spritesheet import AssetsProvider
from window import Window


if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)  # pylint: disable=E0401, E1101, W0212

    window = Window(*Settings().get_window_size())

    asset_provider = AssetsProvider()

    game_manager = GameManager(window, asset_provider)

    window.loop(game_manager.game_loop)
