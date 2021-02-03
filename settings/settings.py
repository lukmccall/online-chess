from extensions import SingletonMeta


class Settings(metaclass=SingletonMeta):
    def __init__(self):
        self._window_size = (640, 640)
        self._chess_assets_path = "assets/chess-pieces-sprite.png"
        self._light_squares_color = (251, 196, 117)
        self._dark_squares_color = (139, 69, 0)
        self._highlights_possible_moves_color = (244, 0, 0)
        self._highlights_possible_moves_size = 12
        self._text_color = (255, 0, 0)
        self._mtu = 1024 * 4

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

    def get_mtu(self):
        return self._mtu

    # self._calc_cell_size()
    #
    # def set_window_size(self, width, height):
    #     self.window_size = (width, height)
    #     self._calc_cell_size()
    #
    #
    # def get_cell_size(self):
    #     return self.cell_size
    #
    # def _calc_cell_size(self):
    #     w, h = self.window_size
    #     self.cell_size = 25, 25
