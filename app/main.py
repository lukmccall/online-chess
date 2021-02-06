"""
A main entry point of the app
"""
import sys
import os

from game import GameManager, AssetsProvider, Window
from settings import Settings


if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        # noinspection PyProtectedMember
        # pyre-ignore[16]:
        os.chdir(sys._MEIPASS)  # pylint: disable=E0401, E1101, W0212

    window = Window(*Settings().get_window_size())

    asset_provider = AssetsProvider()

    game_manager = GameManager(window, asset_provider)

    window.loop(game_manager.game_loop)
