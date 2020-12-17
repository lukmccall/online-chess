from singletonmetaclass import SingletonMeta


class Settings(metaclass=SingletonMeta):

    def __init__(self):
        self.window_size = (640, 640)

    def set_window_size(self, width, height):
        self.window_size = (width, height)

    def get_window_size(self):
        return self.window_size
