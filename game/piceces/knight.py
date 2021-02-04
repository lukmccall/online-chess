from .chesspiece import ChessPiece


class Knight(ChessPiece):

    def __init__(self, image, position, team, cell_size):
        super().__init__(image, position, team, cell_size)
