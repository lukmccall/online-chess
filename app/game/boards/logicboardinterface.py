from typing import Optional, Iterator

import chess

from langextensions import Interface, abstract


class LogicBoardInterface(metaclass=Interface):
    @abstract
    def get_possible_moves_from(self, row, col) -> Iterator[chess.Move]:
        pass

    @abstract
    def execute_move(self, move: chess.Move):
        pass

    @abstract
    def is_checkmate(self) -> bool:
        pass

    @abstract
    def is_stalemate(self) -> bool:
        pass

    @abstract
    def generate_move(self, from_row, from_col, to_row, to_col) -> Optional[chess.Move]:
        pass

    @abstract
    def is_game_over(self) -> bool:
        pass

    @abstract
    def is_move_legal(self, move: chess.Move) -> bool:
        pass

    @abstract
    def is_en_passant(self, move: chess.Move) -> bool:
        pass

    @abstract
    def is_castling(self, move: chess.Move) -> bool:
        pass

    @abstract
    def piece_at(self, square: chess.Square) -> chess.Piece:
        pass

    @abstract
    def turn(self) -> chess.Color:
        pass

    @abstract
    def winner(self) -> Optional[chess.Color]:
        pass
