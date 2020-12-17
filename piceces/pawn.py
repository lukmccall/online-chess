from .chesspiece import ChessPiece


class Pawn(ChessPiece):

    def __init__(self, image, position, team):
        super().__init__(image, position, team)
        self.was_moved = False
