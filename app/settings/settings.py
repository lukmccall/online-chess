from langextensions import SingletonMeta


class Settings(metaclass=SingletonMeta):
    def __init__(self):
        self._window_size = (640, 640)
        self._chess_assets_path = "assets/chess-pieces-sprite.png"
        self._light_squares_color = (251, 196, 117)
        self._dark_squares_color = (139, 69, 0)
        self._highlights_possible_moves_color = (244, 0, 0)
        self._highlights_possible_moves_size = 12
        self._text_color = (255, 0, 0)

        self._flip_board = False

    def get_window_size(self):
        return self._window_size

    def get_chess_assets_path(self):
        return self._chess_assets_path

    def get_light_squares_color(self):
        return self._light_squares_color

    def get_dark_squares_color(self):
        return self._dark_squares_color

    def get_highlights_moves_color(self):
        return self._highlights_possible_moves_color

    def get_highlights_moves_size(self):
        return self._highlights_possible_moves_size

    def get_text_color(self):
        return self._text_color

    def get_flip_board(self):
        return self._flip_board

    def set_flip_board(self, to: bool):
        self._flip_board = to
