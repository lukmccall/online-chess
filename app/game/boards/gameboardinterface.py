from typing import Optional, Iterator

from langextensions import Interface, abstract

import chess


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

    @abstract
    def winner(self) -> Optional[chess.Color]:
        pass

    @abstract
    def set_flip(self, new_value: bool):
        pass
