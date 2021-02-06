"""
A module which contains ChessPieceEnum
"""
from enum import Enum


class ChessPieceEnum(Enum):
    """An enum representing the piece type
    """
    PAWN = 0
    KNIGHT = 1
    BISHOP = 2
    ROOK = 3
    QUEEN = 4
    KING = 5
