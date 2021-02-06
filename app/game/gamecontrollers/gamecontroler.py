"""
A module containing the base game controller implementation
"""
from typing import List, Tuple, Optional
import pygame
import chess

from settings import Settings
from constants import Team

from ..boards import GameBoardInterface


class GameController:
    """
    A simple game controller which is used to interact between user and the board.
    This implementation is used in the local game.
    Also this class contains the state of the current game.
    """
    def __init__(self, board: GameBoardInterface, team: Team) -> None:
        self._board = board
        self.team = team
        self._mouse_was_press = False
        self._selected_position: Optional[Tuple[int, int]] = None
        self._possible_moves: Optional[List[chess.Move]] = None

    def prepare(self) -> None:
        """Prepare game controller

        This method is triggered on every frame before the board is drawn
        """
        if Settings().get_flip_board():
            self._board.set_flip(self.team == Team.WHITE)

    def pipe_events(self, events: List[pygame.event.Event]) -> None:
        """Pipes events from pygame to the controller
        """
        self._mouse_was_press = False

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                self._mouse_was_press = True

    def on_move(self, move: chess.Move) -> None:
        """Hook which allow do something after the move was executed
        """

    def action(self) -> None:
        """Executes user actions

        This method is trigger after the board is drawn
        """
        if self._mouse_was_press:
            row, col = self._get_mouse_index()

            piece = self._board.get_piece_at(row, col)
            if piece and piece.team == self.team:
                self._selected_position = (row, col)
                self._possible_moves = list(self._board.get_possible_moves_from(row, col))
            elif self._selected_position:
                legal_move = self._board.generate_move(*self._selected_position, row, col)
                if legal_move:
                    self._board.move(legal_move)
                    self.on_move(legal_move)

                self._selected_position = None
                self._possible_moves = None

        if self._possible_moves:
            self._board.draw_moves(self._possible_moves)

    def _get_mouse_index(self) -> Tuple[int, int]:
        """Gets a mouse board index

        :return: [row, col]
        """
        cursor_position = pygame.mouse.get_pos()
        mouse_x, mouse_y = cursor_position
        width, height = self._board.get_cell_size()
        return mouse_y // width, mouse_x // height
