from collections import defaultdict
from typing import Optional, Iterator

import pygame
import chess

from settings import Settings
from piceces import ChessPiece

from .helper import \
    iterate_over_board_squares, \
    map_piece_types,\
    map_piece_color, \
    map_square_to_index
from .logicboardinterface import LogicBoardInterface
from .logicboard import PythonChessLogicBoard
from .gameboardinterface import GameBoardInterface


class FlippableGroup(pygame.sprite.Group):
    def __init__(self, is_flipped: bool):
        pygame.sprite.Group.__init__(self)
        self.is_flipped = is_flipped

    def draw(self, surface):
        if self.is_flipped:
            sprites = self.sprites()

            to_blits = [(spr.image, self.transform_rect(surface, spr.rect)) for spr in sprites]
            self.spritedict.update(
                zip(
                    sprites,
                    surface.blits(to_blits)
                )
            )

            self.lostsprites = []  # pylint: disable=W0201
        else:
            super().draw(surface)

    @staticmethod
    def transform_rect(
            surface: pygame.surface.Surface,
            rect: pygame.rect.Rect
    ) -> pygame.rect.Rect:
        new_rect = rect.copy()
        new_rect.y = surface.get_height() - rect.y - rect.height

        return new_rect


class Board(GameBoardInterface):
    def __init__(self, surface: pygame.Surface, pieces_factory,
                 logic_board: LogicBoardInterface = None):
        self.surface = surface
        self.logic_board = logic_board if logic_board is not None else PythonChessLogicBoard()

        self.display_board = defaultdict()
        self.pieces_factory = pieces_factory

        self.colors = (Settings().get_light_squares_color(), Settings().get_dark_squares_color())
        self.cell_size = self.surface.get_width() // 8, self.surface.get_height() // 8
        self.is_flipped = True

        for square in iterate_over_board_squares():
            piece = self.logic_board.piece_at(square)
            if piece:
                mapped_piece = map_piece_types(piece.piece_type)
                mapped_color = map_piece_color(piece.color)

                position = map_square_to_index(square)
                py_piece = pieces_factory.crete_piece(
                    mapped_piece,
                    mapped_color,
                    position,
                    self.cell_size
                )

                self.display_board[square] = py_piece

    def draw(self):
        self.draw_board_cells()
        group = FlippableGroup(self.is_flipped)
        for piece in self.display_board.values():
            group.add(piece)
        group.draw(self.surface)

    def draw_board_cells(self):
        width, height = Settings().get_window_size()
        width, height = width // 8, height // 8
        index = 1
        for column in range(8):
            for row in range(8):
                cell = pygame.Rect(row * height, column * width, width + 1, height + 1)
                pygame.draw.rect(self.surface, self.colors[index], cell)
                index = (index - 1) * -1
            index = (index - 1) * -1

    def get_piece_at(self, row, col) -> Optional[ChessPiece]:
        if self.is_flipped:
            row = 7 - row

        index = row * 8 + col
        if index in self.display_board:
            return self.display_board[index]
        return None

    def get_possible_moves_from(self, row, col) -> Iterator[chess.Move]:
        if self.is_flipped:
            row = 7 - row

        return self.logic_board.get_possible_moves_from(row, col)

    def draw_moves(self, moves: [chess.Move]):
        width, height = self.cell_size

        for move in moves:
            target = move.to_square
            row = target // 8
            col = target % 8

            if self.is_flipped:
                row = 7 - row

            top_x = col * width + width / 2
            top_y = row * height + height / 2

            pygame.draw.circle(
                self.surface,
                Settings().get_highlights_moves_color(),
                (top_x, top_y),
                Settings().get_highlights_moves_size()
            )

    def generate_move(self, from_row, from_col, to_row, to_col) -> Optional[chess.Move]:
        if self.is_flipped:
            from_row = 7 - from_row
            to_row = 7 - to_row

        return self.logic_board.generate_move(from_row, from_col, to_row, to_col)

    def move(self, move: chess.Move):
        if not self.logic_board.is_move_legal(move):
            raise AssertionError("Illegal move")

        piece = self.display_board.get(move.from_square)
        self.display_board.pop(move.from_square)

        if self.logic_board.is_en_passant(move):
            sign = 1 if move.from_square < move.to_square else -1
            square_in_front = move.from_square + 8 * sign
            direction = square_in_front - move.to_square

            captured_square = move.from_square - direction

            self.display_board.pop(captured_square)

        new_position = map_square_to_index(move.to_square)

        if move.promotion is not None:
            promoted_piece_type = map_piece_types(move.promotion)
            promoted_piece_color = map_piece_color(
                self.logic_board.piece_at(move.from_square).color
            )
            promoted_piece = self.pieces_factory.crete_piece(
                promoted_piece_type,
                promoted_piece_color,
                new_position,
                self.cell_size
            )
            self.display_board[move.to_square] = promoted_piece
        else:
            piece.move_to(new_position)
            self.display_board[move.to_square] = piece

            if self.logic_board.is_castling(move):
                direction = move.to_square - move.from_square
                if direction > 0:
                    rock = self.display_board.pop(move.to_square // 8 * 8 + 7)
                    self.display_board[move.to_square - 1] = rock
                    rock.move_to(map_square_to_index(move.to_square - 1))
                else:
                    rock = self.display_board.pop(move.to_square // 8 * 8)
                    self.display_board[move.to_square + 1] = rock
                    rock.move_to(map_square_to_index(move.to_square + 1))

        self.logic_board.execute_move(move)

    def turn(self):
        return map_piece_color(self.logic_board.turn())

    def is_checkmate(self):
        return self.logic_board.is_checkmate()

    def is_stalemate(self):
        return self.logic_board.is_stalemate()

    def is_game_over(self):
        return self.logic_board.is_game_over()

    def winner(self) -> Optional[chess.Color]:
        return self.logic_board.winner()

    def set_flip(self, new_value: bool):
        self.is_flipped = new_value
