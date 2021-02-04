import socket
import pygame_menu

from settings import Settings
from multiplayer import NoneBlockingSocketWrapper

from .joininggamestate import JoiningGameState
from .localgamestate import LocalGameState
from .menubasestate import MenuBaseState
from ..gamemanagers import GameManagerInterface


class MainMenuState(MenuBaseState):
    def __init__(self, game_manager: GameManagerInterface):
        super().__init__(game_manager)
        self.menu = pygame_menu.Menu(
            game_manager.get_window().height,
            game_manager.get_window().width,
            "Online Chess",
            theme=pygame_menu.themes.THEME_DARK,
            enabled=False
        )

        self.menu.add_button("Play", self.on_new_local_game)
        self.menu.add_button("Multiplayer", self.on_multiplayer_game)
        self.menu.add_vertical_margin(20)
        self.menu.add_selector(
            "Flip board",
            [("No", False), ("Yes", True)],
            default=1 if Settings().get_flip_board() else 0,
            onchange=lambda _, to: Settings().set_flip_board(to)
        )
        self.menu.add_vertical_margin(20)
        self.menu.add_button("Quit", self.on_end)

    def on_new_local_game(self):
        self.game_manager.change_state(LocalGameState(self.game_manager))

    def on_end(self):
        self.game_manager.window.is_running = False

    def on_multiplayer_game(self):
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.connect(("127.0.0.1", 5555))
        except ConnectionRefusedError as connection_error:
            print(connection_error)
            return

        self.game_manager.change_state(
            JoiningGameState(
                self.game_manager, NoneBlockingSocketWrapper(soc)
            )
        )
