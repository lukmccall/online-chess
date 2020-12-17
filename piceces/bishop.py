from .chesspiece import ChessPiece


class Bishop(ChessPiece):

    def __init__(self, image, position, team):
        super().__init__(image, position, team)