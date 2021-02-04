import pygame

from settings import Settings
from constants import Team
from multiplayer import SocketWrapperInterface, MoveMessage, MessageType

from .gamecontroler import GameController
from ..boards import GameBoardInterface


class MultiplayerGameController(GameController):
    def __init__(
            self,
            board: GameBoardInterface,
            team: Team,
            connection: SocketWrapperInterface
    ):
        super().__init__(board, team)
        self.connection = connection
        self.message = None

    def prepare(self):
        if Settings().get_flip_board():
            self.board.set_flip(self.team == Team.WHITE)

    def pipe_events(self, events: [pygame.event.Event]):
        if not self.team == self.board.turn():
            self.message = self.connection.receive()
            return

        super().pipe_events(events)

    def action(self):
        if not self.team == self.board.turn():
            if self.message is not None:
                if self.message.type == MessageType.MOVE:
                    move = self.message.move
                    self.board.move(move)
                self.message = None
            return

        super().action()

    def on_move(self, move):
        self.connection.send(MoveMessage(move))
