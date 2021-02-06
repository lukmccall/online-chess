"""
A module containing LocalGameState
"""
from typing import Optional, cast
from constants import Team
from multiplayer import SocketWrapperInterface

from .basegamestate import BaseGameState
from ..gamecontrollers import GameController, MultiplayerGameController
from ..gamemanagers import GameManagerInterface


class OnlineGameState(BaseGameState):
    """
    State where user in in the online game.
    """
    def __init__(
        self,
        game_manager: GameManagerInterface,
        socket: SocketWrapperInterface,
        team: Team
    ) -> None:
        super().__init__(game_manager)

        self._socket = socket
        self._team = team
        self._game_controller: Optional[GameController] = None

    def on_state_exit(self) -> None:
        super().on_state_exit()
        self._socket.close()

    def get_game_controller(self) -> GameController:
        assert self._game_controller
        return cast(GameController, self._game_controller)

    def on_state_start(self) -> None:
        super().on_state_start()
        self._game_controller = MultiplayerGameController(
            self.get_board(),
            self._team,
            self._socket
        )
