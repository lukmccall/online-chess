from dataclasses import dataclass, field
from enum import Enum
import chess

from constants import Team


class MessageType(Enum):
    SET_TEAM = 0
    START = 1
    MOVE = 2


@dataclass
class Message:
    type: MessageType = field(init=False)

    def __str__(self):
        return "[{}]".format(self.type)


@dataclass
class StartMessage(Message):
    type = MessageType.START


@dataclass
class SetTeamMessage(Message):
    type = MessageType.SET_TEAM
    team: Team

    def __str__(self):
        return "{} {}".format(super().__str__(), self.team)


@dataclass
class MoveMessage(Message):
    type = MessageType.MOVE
    move: chess.Move

    def __str__(self):
        return "{} {}".format(super().__str__(), self.move)
