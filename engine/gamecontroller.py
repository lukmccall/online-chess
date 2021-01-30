from .board import Board
from piceces import Team
import pygame
from settings import Settings


class GameController:
    def __init__(self, board: Board, team: Team):
        self.board = board
        self.team = team
        self.mouse_was_press = False
        self.selected_position = None
        self.possible_moves = None

    def pipe_events(self, events: [pygame.event.Event]):
        self.mouse_was_press = False

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_was_press = True

    def action(self):
        if self.mouse_was_press:
            cursor_position = pygame.mouse.get_pos()
            mouse_x, mouse_y = cursor_position
            width, height = Settings().get_cell_size()
            row, col = (mouse_y // width, mouse_x // height)

            piece = self.board.get_piece_at(row, col)

            if piece and piece.team == self.team:
                self.selected_position = (row, col)
                self.possible_moves = list(self.board.get_possible_moves_from(row, col))
            elif self.selected_position:
                legal_move = self.board.can_move(*self.selected_position, row, col)
                if legal_move:
                    self.board.move(legal_move)

                self.selected_position = None
                self.possible_moves = None

        if self.possible_moves:
            self.board.draw_moves(self.possible_moves)
