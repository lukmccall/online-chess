from singletonmetaclass import SingletonMeta


class Settings(metaclass=SingletonMeta):

    def __init__(self):
        self.window_size = (640, 640)
        self.board_size = 8
        self._calc_cell_size()

    def set_window_size(self, width, height):
        self.window_size = (width, height)
        self._calc_cell_size()

    def get_window_size(self):
        return self.window_size

    def get_cell_size(self):
        return self.cell_size

    def get_board_size(self):
        return self.board_size

    def _calc_cell_size(self):
        w, h = self.window_size
        self.cell_size = (w // self.board_size, h // self.board_size)
