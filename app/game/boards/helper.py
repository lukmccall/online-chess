"""
A module which contains a helpers methods used in the board class
"""
from typing import Iterator, Tuple
import chess

from constants import Team

from ..piceces import ChessPieceEnum

piece_type_mapper = {
    chess.PAWN: ChessPieceEnum.PAWN,
    chess.KNIGHT: ChessPieceEnum.KNIGHT,
    chess.BISHOP: ChessPieceEnum.BISHOP,
    chess.ROOK: ChessPieceEnum.ROOK,
    chess.QUEEN: ChessPieceEnum.QUEEN,
    chess.KING: ChessPieceEnum.KING
}


def iterate_over_board_squares() -> Iterator[chess.Square]:
    """Returns an iterator of all board squares

    :return: An board square iterator
    """
    for square in chess.SQUARES:
        yield square


def map_piece_types(piece_type: chess.PieceType) -> ChessPieceEnum:
    """Maps pieces type

    :param piece_type: Piece type from chess package
    :return Piece type from constants package
    :raises TypeError: if provided type is incorrect
    """
    if piece_type not in piece_type_mapper:
        raise TypeError("Invalid piece_type")
    return piece_type_mapper[piece_type]


def map_piece_color(piece_color: chess.Color) -> Team:
    """Maps piece color

    :param piece_color: Piece color from chess package
    :return: Piece color(Team) from game.pieces package
    """
    if piece_color == chess.WHITE:
        return Team.WHITE
    return Team.BLACK


def map_square_to_index(square: chess.Square) -> Tuple[int, int]:
    """Maps square to index

    :param square: Square to map
    :returns: A tuple which contains row and col value
    """
    return square // 8, square % 8
