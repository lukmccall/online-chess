from collections import defaultdict
from typing import Optional

import pygame
import chess
from .helper import iterate_over_board_squares, map_piece_types, map_piece_color, map_square_to_index
from settings import Settings
from piceces import ChessPiece, Team

light_brown = (251, 196, 117)
dark_brown = (139, 69, 0)

colors = (light_brown, dark_brown)


class Board(pygame.sprite.Group):
    def __init__(self, surface: pygame.Surface, pieces_type_images):
        super().__init__()
        self.surface = surface
        self.logicBoard = chess.Board()

        self.displayBoard = defaultdict()
        self.pieces_type_images = pieces_type_images

        for square in iterate_over_board_squares():
            piece = self.logicBoard.piece_at(square)
            if piece:
                mapped_piece = map_piece_types(piece.piece_type)
                mapped_color = map_piece_color(piece.color)

                index = map_square_to_index(square)
                py_piece = mapped_piece.get_class(pieces_type_images[(mapped_piece, mapped_color)], index, mapped_color)

                self.displayBoard[square] = py_piece
                super().add(py_piece)

    def draw(self) -> None:
        self.draw_board_cells()
        super().draw(self.surface)

    def draw_board_cells(self):
        width, height = Settings().get_window_size()
        width, height = width // 8, height // 8
        index = 1  # toswitchcolors (index - 1) * -1
        for column in range(8):
            for row in range(8):
                cell = pygame.Rect(row * height, column * width, width + 1, height + 1)
                pygame.draw.rect(self.surface, colors[index], cell)
                index = (index - 1) * -1
            index = (index - 1) * -1

    def get_piece_at(self, row, col) -> Optional[ChessPiece]:
        index = row * Settings().get_board_size() + col
        if index in self.displayBoard:
            return self.displayBoard[index]
        return None

    def get_possible_moves_from(self, row, col) -> [chess.Move]:
        mask = 1 << row * Settings().get_board_size() + col
        return self.logicBoard.generate_legal_moves(mask, chess.BB_ALL)

    def draw_moves(self, moves: [chess.Move]):
        width, height = Settings().get_cell_size()

        for move in moves:
            target = move.to_square
            row = target // Settings().get_board_size()
            col = target % Settings().get_board_size()

            x = col * width + width / 2
            y = row * height + height / 2
            pygame.draw.circle(self.surface, (255, 0, 0), (x, y), 15)

    def can_move(self, from_row, from_col, to_row, to_col) -> Optional[chess.Move]:
        from_mask = 1 << from_row * Settings().get_board_size() + from_col
        to_mask = 1 << to_row * Settings().get_board_size() + to_col

        moves = list(self.logicBoard.generate_legal_moves(from_mask, to_mask))
        if len(moves) == 1:
            return moves[0]
        elif len(moves) > 1:
            return moves[0]  # TODO: promotion

        return None

    def move(self, move: chess.Move):
        if not self.logicBoard.is_legal(move):
            raise AssertionError("Illegal move")

        piece = self.displayBoard.get(move.from_square)
        self.displayBoard.pop(move.from_square)

        if move.to_square in self.displayBoard:
            self.remove(self.displayBoard[move.to_square])

        if self.logicBoard.is_en_passant(move):
            sign = 1 if move.from_square < move.to_square else -1
            square_in_front = move.from_square + 8 * sign
            direction = square_in_front - move.to_square

            captured_square = move.from_square - direction

            self.remove(self.displayBoard[captured_square])
            self.displayBoard.pop(captured_square)

        new_position = map_square_to_index(move.to_square)
        if move.promotion is not None:
            promoted_piece_type = map_piece_types(move.promotion)
            promoted_piece_color = map_piece_color(self.logicBoard.color_at(move.from_square))
            promoted_piece = promoted_piece_type.get_class(self.pieces_type_images[(promoted_piece_type, promoted_piece_color)], new_position, promoted_piece_color)
            self.displayBoard[move.to_square] = promoted_piece

            self.remove(piece)
            self.add(promoted_piece)
        else:
            piece.move_to(new_position)
            self.displayBoard[move.to_square] = piece

        self.logicBoard.push(move)

    def turn(self):
        return map_piece_color(self.logicBoard.turn)
