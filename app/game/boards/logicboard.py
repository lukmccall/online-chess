from typing import Optional, Iterator

import chess

from .logicboardinterface import LogicBoardInterface


class PythonChessLogicBoard(LogicBoardInterface):
    def __init__(self):
        self.board = chess.Board()

    def get_possible_moves_from(self, row, col) -> Iterator[chess.Move]:
        mask = 1 << row * 8 + col
        return self.board.generate_legal_moves(mask, chess.BB_ALL)

    def generate_move(self, from_row, from_col, to_row, to_col) -> Optional[chess.Move]:
        from_mask = 1 << from_row * 8 + from_col
        to_mask = 1 << to_row * 8 + to_col

        moves = list(self.board.generate_legal_moves(from_mask, to_mask))
        if len(moves) >= 1:
            return moves[0]

        if from_mask & chess.BB_BACKRANKS and to_mask & chess.BB_BACKRANKS:
            move = chess.Move(to_square=from_row * 8 + to_col, from_square=from_row * 8 + from_col)
            if self.board.is_castling(move) and self.board.is_legal(move):
                return move

        return None

    def execute_move(self, move: chess.Move):
        self.board.push(move)

    def is_checkmate(self) -> bool:
        return self.board.is_checkmate()

    def is_stalemate(self) -> bool:
        return self.board.is_stalemate()

    def is_game_over(self) -> bool:
        return self.board.is_game_over()

    def is_move_legal(self, move: chess.Move) -> bool:
        return self.board.is_legal(move)

    def is_en_passant(self, move: chess.Move) -> bool:
        return self.board.is_en_passant(move)

    def is_castling(self, move: chess.Move) -> bool:
        return self.board.is_castling(move)

    def piece_at(self, square: chess.Square) -> Optional[chess.Piece]:
        return self.board.piece_at(square)

    def turn(self) -> chess.Color:
        return self.board.turn

    def winner(self) -> Optional[chess.Color]:
        if not self.board.is_game_over():
            return None

        result = self.board.result()

        if result == "1/2-1/2":
            return None

        if result == "1-0":
            return chess.WHITE

        if result == "0-1":
            return chess.BLACK

        return None
