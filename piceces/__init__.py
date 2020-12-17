from enum import Enum

from .chesspiece import *
from .pawn import *
from .knight import *
from .bishop import *
from .rook import *
from .queen import *
from .king import *


class ChessPieceEnum(Enum):
    PAWN = Pawn
    KNIGHT = Knight
    BISHOP = Bishop
    ROOK = Rook
    QUEEN = Queen
    KING = King

    @property
    def get_class(self) -> type(ChessPiece):
        return self.value
