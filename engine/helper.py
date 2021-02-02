import chess

from piceces import ChessPieceEnum, Team

piece_type_mapper = {
    chess.PAWN: ChessPieceEnum.PAWN,
    chess.KNIGHT: ChessPieceEnum.KNIGHT,
    chess.BISHOP: ChessPieceEnum.BISHOP,
    chess.ROOK: ChessPieceEnum.ROOK,
    chess.QUEEN: ChessPieceEnum.QUEEN,
    chess.KING: ChessPieceEnum.KING
}


def iterate_over_board_squares():
    for square in chess.SQUARES:
        yield square


def map_piece_types(piece_type: chess.PieceType) -> ChessPieceEnum:
    if piece_type not in piece_type_mapper:
        raise TypeError("Invalid piece_type")
    return piece_type_mapper[piece_type]


def map_piece_color(piece_color: chess.Color):
    if piece_color == chess.WHITE:
        return Team.WHITE
    return Team.BLACK


def map_square_to_index(square: chess.Square):
    return square // 8, square % 8
