import pygame

import multiplayer as mp
from piceces import Team
from .gameboard import Board


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
            width, height = self.board.cell_size
            row, col = (mouse_y // width, mouse_x // height)

            piece = self.board.get_piece_at(row, col)

            if piece and piece.team == self.team:
                self.selected_position = (row, col)
                self.possible_moves = list(self.board.get_possible_moves_from(row, col))
            elif self.selected_position:
                legal_move = self.board.generate_move(*self.selected_position, row, col)
                if legal_move:
                    self.board.move(legal_move)

                self.selected_position = None
                self.possible_moves = None

        if self.possible_moves:
            self.board.draw_moves(self.possible_moves)

        if self.team == Team.WHITE:
            self.board.flip()


class MultiplayerGameController:
    def __init__(self, board: Board, team: Team, connection: mp.SocketWrapperInterface):
        self.board = board
        self.team = team
        self.connection = connection
        self.mouse_was_press = False
        self.selected_position = None
        self.possible_moves = None
        self.message = None

    def pipe_events(self, events: [pygame.event.Event]):
        self.mouse_was_press = False
        if not self.team == self.board.turn():
            self.message = self.connection.receive()
            return

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self.mouse_was_press = True

    def action(self):
        if not self.team == self.board.turn():
            if self.message is not None:
                print(self.message)
                if self.message.type == mp.MessageType.MOVE:
                    move = self.message.move
                    self.board.move(move)
                self.message = None
            return

        if self.mouse_was_press:
            cursor_position = pygame.mouse.get_pos()
            mouse_x, mouse_y = cursor_position
            width, height = self.board.cell_size
            row, col = (mouse_y // width, mouse_x // height)

            piece = self.board.get_piece_at(row, col)

            if piece and piece.team == self.team:
                self.selected_position = (row, col)
                self.possible_moves = list(self.board.get_possible_moves_from(row, col))
            elif self.selected_position:
                legal_move = self.board.generate_move(*self.selected_position, row, col)
                if legal_move:
                    self.board.move(legal_move)
                    self.connection.send(mp.MoveMessage(legal_move))

                self.selected_position = None
                self.possible_moves = None

        if self.possible_moves:
            self.board.draw_moves(self.possible_moves)
