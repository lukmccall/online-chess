"""
A module containing the StateInterface
"""
from typing import List
import pygame

from langextensions import Interface, abstract


class StateInterface(metaclass=Interface):
    """
    An common interface for all game states
    """
    @abstract
    def on_state_exit(self) -> None:
        """A life cycle method which should be triggered
        on the state exit
        """

    @abstract
    def on_state_start(self) -> None:
        """A life cycle method which should be triggered
        on the state start
        """

    @abstract
    def on_game_loop(self, events: List[pygame.event.Event]) -> None:
        """Method should be triggered on every game frame

        :param events: List of pygame events
        """
