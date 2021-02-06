"""
This module contains the base state for all states used in this app
"""
from typing import List
import pygame

from .stateinterface import StateInterface
from ..gamemanagers import GameManagerInterface
from ..assets import PiecesFactory


class BaseState(StateInterface):
    """
    A abstract class of the game state that providing shortcut methods
    and storing game manager instance
    """
    def __init__(self, game_manager: GameManagerInterface) -> None:
        self._game_manager = game_manager

    def get_display(self) -> pygame.Surface:
        """Gets display surface

         :return: Surface
         """
        return self._game_manager.get_window().game_display

    def get_pieces_factory(self) -> PiecesFactory:
        """Gets pieces factory from game manager

        :return: PiecesFactory
        """
        asset_provider = self._game_manager.get_asset_provider()
        return asset_provider.get_pieces_factory()

    def on_state_exit(self) -> None:
        pass

    def on_state_start(self) -> None:
        pass

    def on_game_loop(self, events: List[pygame.event.Event]) -> None:
        pass
