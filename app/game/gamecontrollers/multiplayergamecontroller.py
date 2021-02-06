"""
A module which contains the multiplayer version of the game controller
"""
from typing import List
import pygame

from settings import Settings
from constants import Team
from multiplayer import SocketWrapperInterface, MoveMessage, MessageType

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
    ):
        super().__init__(board, team)
        self._connection = connection
        self._message = None

    def prepare(self):
        if Settings().get_flip_board():
            self._board.set_flip(self.team == Team.WHITE)

    def pipe_events(self, events: List[pygame.event.Event]):
        if not self.team == self._board.turn():
            self._message = self._connection.receive()
            return

        super().pipe_events(events)

    def action(self):
        if not self.team == self._board.turn():
            if self._message is not None:
                if self._message.type == MessageType.MOVE:
                    move = self._message.move
                    self._board.move(move)
                self._message = None
            return

        super().action()

    def on_move(self, move):
        self._connection.send(MoveMessage(move))
