from engine import GameManager
from settings import Settings
from spritesheet import AssetsProvider
from window import Window
import sys
import os

if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

window = Window(*Settings().get_window_size())

asset_provider = AssetsProvider()

game_manager = GameManager(window, asset_provider)

window.loop(game_manager.game_loop)
