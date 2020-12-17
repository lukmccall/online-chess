from .chesspiece import ChessPiece


class King(ChessPiece):

    def __init__(self, image, position, team):
        super().__init__(image, position, team)