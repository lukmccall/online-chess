from typing import List

import pygame

from .gamemanagerinterface import GameManagerInterface
from ..states import StateInterface, MainMenuState
from ..assets import AssetsProvider
from ..window import Window


class GameManager(GameManagerInterface):
    def __init__(self, window: Window, asset_provider: AssetsProvider):
        self.window = window
        self.asset_provider = asset_provider
        self.state = None
        self.go_to_main_state()

    def game_loop(self, events: List[pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.window.is_running = False
                self.state.on_state_exit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.change_state(MainMenuState(self))
                return
        try:
            self.state.on_game_loop(events)
        except Exception as exception:  # pylint: disable=W0703
            print(exception)
            self.change_state(MainMenuState(self))

    def get_window(self) -> Window:
        return self.window

    def get_asset_provider(self) -> AssetsProvider:
        return self.asset_provider

    def change_state(self, new_state: StateInterface):
        if self.state is not None:
            self.state.on_state_exit()
        self.state = new_state
        self.state.on_state_start()

        self.state.on_game_loop([])

    def go_to_main_state(self):
        self.change_state(MainMenuState(self))
