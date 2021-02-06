"""
A module which defines the multiplayer protocol
"""
from typing import Union
from dataclasses import dataclass, field
from enum import Enum
import chess

from constants import Team


class MessageType(Enum):
    """
    An enum representing message types
    """
    SET_TEAM = 0
    START = 1
    MOVE = 2


@dataclass
class Message:
    """
    Base class of all messages
    """
    type: MessageType = field(init=False)

    def __str__(self) -> str:
        return "[{}]".format(self.type)


@dataclass
class StartMessage(Message):
    """
    A start message
    """
    def __post_init__(self) -> None:
        self.type = MessageType.START


@dataclass
class SetTeamMessage(Message):
    """
    Set team message
    """
    team: Team

    def __post_init__(self) -> None:
        self.type = MessageType.SET_TEAM

    def __str__(self) -> str:
        return "{} {}".format(super().__str__(), self.team)


@dataclass
class MoveMessage(Message):
    """
    Message which represents move
    """
    move: chess.Move

    def __post_init__(self) -> None:
        self.type = MessageType.MOVE

    def __str__(self) -> str:
        return "{} {}".format(super().__str__(), self.move)


AllMessageType = Union[StartMessage, SetTeamMessage, MoveMessage]
