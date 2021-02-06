"""
This module contains settings singleton class
"""
from typing import Tuple
from langextensions import SingletonMeta


ColorTuple = Tuple[int, int, int]


class Settings(metaclass=SingletonMeta):  # pylint: disable=R0902
    """
    Singleton class which contains all configurable settings.
    """
    def __init__(self) -> None:
        self._window_size = (640, 640)
        self._chess_assets_path = "assets/chess-pieces-sprite.png"
        self._light_squares_color = (251, 196, 117)
        self._dark_squares_color = (139, 69, 0)
        self._highlights_possible_moves_color = (244, 0, 0)
        self._highlights_possible_moves_size = 12
        self._text_color = (255, 0, 0)

        self._flip_board = False

    def get_window_size(self) -> Tuple[int, int]:
        """Gets window size

        :return: Window size
        """
        return self._window_size

    def get_chess_assets_path(self) -> str:
        """Gets asset path

        :return: Path to chess asset sprite
        """
        return self._chess_assets_path

    def get_light_squares_color(self) -> ColorTuple:
        """Gets light squares color

        :return: Color of light squares
        """
        return self._light_squares_color

    def get_dark_squares_color(self) -> ColorTuple:
        """Gets dar squares color

        :return: Color of dar squares
        """
        return self._dark_squares_color

    def get_highlights_moves_color(self) -> ColorTuple:
        """Gets highlight color

        :return: Highlight color
        """
        return self._highlights_possible_moves_color

    def get_highlights_moves_size(self) -> int:
        """Gets highlight size

        :return: Size of highlight
        """
        return self._highlights_possible_moves_size

    def get_text_color(self) -> ColorTuple:
        """Gets text color

        :return: Text color
        """
        return self._text_color

    def get_flip_board(self) -> bool:
        """Gets flip board option

        :return: Bool
        """
        return self._flip_board

    def set_flip_board(self, new_value: bool) -> None:
        """Sets the flip board option
        """
        self._flip_board = new_value
