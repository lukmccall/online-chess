"""
A module containing JoiningGameState
"""
from typing import List
import pygame

from multiplayer import SocketWrapperInterface, MessageType

from .menubasestate import MenuBaseState
from .onlinegamestate import OnlineGameState
from ..gamemanagers import GameManagerInterface


class JoiningGameState(MenuBaseState):
    """
    A state where user is looking for new online player game
    """
    def __init__(
            self,
            game_manager: GameManagerInterface,
            socket: SocketWrapperInterface
    ):
        super().__init__(game_manager)

        self._socket = socket

        self._menu.add_label("Waiting for connection")
        self._menu.add_button("Quit", self.on_end)

        self._preserve_socket = False
        self._team = None

    def on_state_exit(self) -> None:
        super().on_state_exit()

        if not self._preserve_socket:
            self._socket.close()

    def on_game_loop(self, events: List[pygame.event.Event]) -> None:
        message = self._socket.receive()
        if message is None:
            super().on_game_loop(events)
            return

        if self._team is None:
            if message.type == MessageType.SET_TEAM:
                self._team = message.team
            else:
                raise AssertionError("Expect [SET_TEAM] message but got {}.".format(message))
        else:
            if message.type == MessageType.START:
                self._preserve_socket = True
                self._game_manager.change_state(
                    OnlineGameState(
                        self._game_manager,
                        self._socket,
                        self._team
                    )
                )
                return

            raise AssertionError("Expect [START] message but got {}.".format(message))

        super().on_game_loop(events)

    def on_end(self) -> None:
        """Methods which is called when
        the user clicks on the end button
        """
        self._game_manager.go_to_main_state()
