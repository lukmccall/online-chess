import pygame

from ..gamemanagers import GameManagerInterface
from .stateinterface import StateInterface


class BaseState(StateInterface):
    def __init__(self, game_manager: GameManagerInterface):
        self.game_manager = game_manager

    def get_display(self) -> pygame.surface.Surface:
        return self.game_manager.get_window().game_display

    def get_pieces_factory(self):
        asset_provider = self.game_manager.get_asset_provider()
        return asset_provider.get_pieces_factory()

    def on_state_exit(self):
        pass

    def on_state_start(self):
        pass

    def on_game_loop(self, events: [pygame.event.Event]):
        pass
