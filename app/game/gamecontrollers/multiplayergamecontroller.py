"""
A module which contains the multiplayer version of the game controller
"""
from typing import List, Optional, cast
import pygame
import chess

from constants import Team
from multiplayer import \
    SocketWrapperInterface, \
    MoveMessage,\
    MessageType,\
    AllMessageType

from .gamecontroler import GameController
from ..boards import GameBoardInterface


class MultiplayerGameController(GameController):
    """
    Implementation of multiplayer game controller using sockets.
    This class extends GameController.
    """
    def __init__(
        self,
        board: GameBoardInterface,
        team: Team,
        connection: SocketWrapperInterface
    ) -> None:
        super().__init__(board, team)
        self._connection = connection
        self._message: Optional[AllMessageType] = None

    def prepare(self) -> None:
        self._board.set_flip(self.team == Team.WHITE)

    def pipe_events(self, events: List[pygame.event.Event]) -> None:
        if not self.team == self._board.turn():
            self._message = self._connection.receive()
            return

        super().pipe_events(events)

    def action(self) -> None:
        if not self.team == self._board.turn():
            message = self._message
            if message is not None:
                if message.type == MessageType.MOVE:
                    casted_message = cast(MoveMessage, message)
                    self._board.move(casted_message.move)
                self._message = None
            return

        super().action()

    def on_move(self, move: chess.Move) -> None:
        self._connection.send(MoveMessage(move))
