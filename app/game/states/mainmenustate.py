"""
This module contains MainMenuState
"""
import socket

from settings import Settings
from multiplayer import NoneBlockingSocketWrapper

from .joininggamestate import JoiningGameState
from .localgamestate import LocalGameState
from .menubasestate import MenuBaseState
from ..gamemanagers import GameManagerInterface


class MainMenuState(MenuBaseState):
    """
    State where user is in the main menu.
    Base state of the app.
    """
    def __init__(self, game_manager: GameManagerInterface):
        super().__init__(game_manager)
        self._menu.add_button("Play", self.on_new_local_game)
        self._menu.add_button("Multiplayer", self.on_multiplayer_game)
        self._menu.add_vertical_margin(20)
        self._menu.add_selector(
            "Flip board",
            [("No", False), ("Yes", True)],
            default=1 if Settings().get_flip_board() else 0,
            onchange=lambda _, to: Settings().set_flip_board(to)
        )
        self._menu.add_vertical_margin(20)
        self._menu.add_button("Quit", self.on_end)

    def on_new_local_game(self) -> None:
        """Methods called when user selects new local game from menu
        """
        self._game_manager.change_state(LocalGameState(self._game_manager))

    def on_end(self) -> None:
        """Methods called when user selects quit button
        """
        self._game_manager.window.stop()

    def on_multiplayer_game(self) -> None:
        """Methods called when user selects new multiplayer game from menu
        """
        try:
            soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            soc.connect(("127.0.0.1", 5555))
        except ConnectionRefusedError as connection_error:
            print(connection_error)
            return

        self._game_manager.change_state(
            JoiningGameState(
                self._game_manager, NoneBlockingSocketWrapper(soc)
            )
        )
