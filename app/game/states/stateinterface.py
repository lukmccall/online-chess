from typing import List
import pygame

from langextensions import Interface, abstract


class StateInterface(metaclass=Interface):
    @abstract
    def on_state_exit(self):
        pass

    @abstract
    def on_state_start(self):
        pass

    @abstract
    def on_game_loop(self, events: List[pygame.event.Event]):
        pass
