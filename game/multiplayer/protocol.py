from enum import Enum
from piceces import Team
import chess


class MessageType(Enum):
    SET_TEAM = 0
    START = 1
    MOVE = 2


class Message:
    def __init__(self, message_type: MessageType):
        self.type = message_type

    def __str__(self):
        return "[{}]".format(self.type)


class SetTeamMessage(Message):
    def __init__(self, team: Team):
        super().__init__(MessageType.SET_TEAM)
        self.team = team

    def __str__(self):
        return "{} {}".format(super().__str__(), self.team)


class StartMessage(Message):
    def __init__(self):
        super().__init__(MessageType.START)


class MoveMessage(Message):
    def __init__(self, move: chess.Move):
        super(MoveMessage, self).__init__(MessageType.MOVE)
        self.move = move

    def __str__(self):
        return "{} {}".format(super().__str__(), self.move)
