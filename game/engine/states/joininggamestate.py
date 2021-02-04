import pygame
import pygame_menu

from multiplayer import SocketWrapperInterface, MessageType

from .menubasestate import MenuBaseState
from .onlinegamestate import OnlineGameState
from ..gamemanagers import GameManagerInterface


class JoiningGameState(MenuBaseState):
    def __init__(
            self,
            game_manager: GameManagerInterface,
            socket: SocketWrapperInterface
    ):
        super().__init__(game_manager)

        self.socket = socket

        self.menu = pygame_menu.Menu(
            game_manager.window.height,
            game_manager.window.width,
            "Online Chess",
            theme=pygame_menu.themes.THEME_DARK,
            enabled=False
        )

        self.menu.add_label("Waiting for connection")
        self.menu.add_button("Quit", self.on_end)

        self.preserve_socket = False
        self.team = None

    def on_state_exit(self):
        super().on_state_exit()

        if not self.preserve_socket:
            self.socket.close()

    def on_game_loop(self, events: [pygame.event.Event]):
        message = self.socket.receive()
        if message is None:
            return

        if self.team is None:
            if message.type == MessageType.SET_TEAM:
                self.team = message.team
            else:
                raise AssertionError("Expect [SET_TEAM] message but got {}.".format(message))
        else:
            if message.type == MessageType.START:
                self.preserve_socket = True
                self.game_manager.change_state(
                    OnlineGameState(
                        self.game_manager,
                        self.socket,
                        self.team
                    )
                )
            else:
                raise AssertionError("Expect [START] message but got {}.".format(message))

        super().on_game_loop(events)

    def on_end(self):
        self.game_manager.go_to_main_state()
