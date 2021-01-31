from collections import defaultdict
from typing import Optional, Iterator
from extensions import Interface, abstract
import pygame
import chess
from .helper import iterate_over_board_squares, map_piece_types, map_piece_color, map_square_to_index
from .logicboard import LogicBoardInterface, PythonChessLogicBoard
from settings import Settings
from piceces import ChessPiece

light_brown = (251, 196, 117)
dark_brown = (139, 69, 0)

colors = (light_brown, dark_brown)


class GameBoardInterface(metaclass=Interface):
    @abstract
    def get_possible_moves_from(self, row, col) -> Iterator[chess.Move]:
        pass

    @abstract
    def generate_move(self, from_row, from_col, to_row, to_col) -> Optional[chess.Move]:
        pass

    @abstract
    def draw(self):
        pass

    @abstract
    def draw_moves(self, moves: [chess.Move]):
        pass

    @abstract
    def is_game_over(self):
        pass

    @abstract
    def turn(self):
        pass


class Board(GameBoardInterface):
    def __init__(self, surface: pygame.Surface, pieces_type_images,
                 logic_board: LogicBoardInterface = None):
        self.surface = surface
        self.logic_board = logic_board if logic_board is not None else PythonChessLogicBoard()

        self.displayBoard = defaultdict()
        self.pieces_type_images = pieces_type_images

        for square in iterate_over_board_squares():
            piece = self.logic_board.piece_at(square)
            if piece:
                mapped_piece = map_piece_types(piece.piece_type)
                mapped_color = map_piece_color(piece.color)

                index = map_square_to_index(square)
                py_piece = mapped_piece.get_class(pieces_type_images[(mapped_piece, mapped_color)], index, mapped_color)

                self.displayBoard[square] = py_piece

    def draw(self):
        self.draw_board_cells()
        group = pygame.sprite.Group()
        for piece in self.displayBoard.values():
            group.add(piece)
        group.draw(self.surface)

    def draw_board_cells(self):
        width, height = Settings().get_window_size()
        width, height = width // 8, height // 8
        index = 1
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

    def get_possible_moves_from(self, row, col) -> Iterator[chess.Move]:
        return self.logic_board.get_possible_moves_from(row, col)

    def draw_moves(self, moves: [chess.Move]):
        width, height = Settings().get_cell_size()

        for move in moves:
            target = move.to_square
            row = target // Settings().get_board_size()
            col = target % Settings().get_board_size()

            x = col * width + width / 2
            y = row * height + height / 2
            pygame.draw.circle(self.surface, (255, 0, 0), (x, y), 15)

    def generate_move(self, from_row, from_col, to_row, to_col) -> Optional[chess.Move]:
        return self.logic_board.generate_move(from_row, from_col, to_row, to_col)

    def move(self, move: chess.Move):
        if not self.logic_board.is_move_legal(move):
            raise AssertionError("Illegal move")

        piece = self.displayBoard.get(move.from_square)
        self.displayBoard.pop(move.from_square)

        if self.logic_board.is_en_passant(move):
            sign = 1 if move.from_square < move.to_square else -1
            square_in_front = move.from_square + 8 * sign
            direction = square_in_front - move.to_square

            captured_square = move.from_square - direction

            self.displayBoard.pop(captured_square)

        new_position = map_square_to_index(move.to_square)

        if move.promotion is not None:
            promoted_piece_type = map_piece_types(move.promotion)
            promoted_piece_color = map_piece_color(self.logic_board.piece_at(move.from_square).color)
            promoted_piece = promoted_piece_type.get_class(
                self.pieces_type_images[(promoted_piece_type, promoted_piece_color)], new_position,
                promoted_piece_color)
            self.displayBoard[move.to_square] = promoted_piece
        else:
            piece.move_to(new_position)
            self.displayBoard[move.to_square] = piece

            if self.logic_board.is_castling(move):
                direction = move.to_square - move.from_square
                if direction > 0:
                    rock = self.displayBoard.pop(move.to_square // 8 * 8 + 7)
                    self.displayBoard[move.to_square - 1] = rock
                    rock.move_to(map_square_to_index(move.to_square - 1))
                else:
                    rock = self.displayBoard.pop(move.to_square // 8 * 8)
                    self.displayBoard[move.to_square + 1] = rock
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