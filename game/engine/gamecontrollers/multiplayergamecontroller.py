import pygame

import multiplayer as mp
from piceces import Team

from .gamecontroler import GameController
from ..boards import GameBoardInterface


class MultiplayerGameController(GameController):
    def __init__(
            self,
            board: GameBoardInterface,
            team: Team,
            connection: mp.SocketWrapperInterface
    ):
        super().__init__(board, team)
        self.connection = connection
        self.message = None

    def pipe_events(self, events: [pygame.event.Event]):
        if not self.team == self.board.turn():
            self.message = self.connection.receive()
            return

        super().pipe_events(events)

    def action(self):
        if not self.team == self.board.turn():
            if self.message is not None:
                if self.message.type == mp.MessageType.MOVE:
                    move = self.message.move
                    self.board.move(move)
                self.message = None
            return

        super().action()
