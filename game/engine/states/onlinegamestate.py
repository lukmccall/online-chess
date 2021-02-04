from piceces import Team
from multiplayer import SocketWrapperInterface

from .basegamestate import BaseGameState
from ..gamecontrollers import GameController, MultiplayerGameController
from ..gamemanagers import GameManagerInterface


class OnlineGameState(BaseGameState):
    def __init__(
            self,
            game_manager: GameManagerInterface,
            socket: SocketWrapperInterface,
            team: Team):
        super().__init__(game_manager)

        self.socket = socket
        self.team = team
        self.game_controller = None

    def on_state_exit(self):
        super().on_state_exit()
        self.socket.close()

    def get_game_controller(self) -> GameController:
        return self.game_controller

    def on_state_start(self):
        super().on_state_start()
        self.game_controller = MultiplayerGameController(
            self.board,
            self.team,
            self.socket
        )
