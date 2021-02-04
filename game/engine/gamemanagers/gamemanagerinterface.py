from window import Window
from extensions import Interface, abstract
from spritesheet import AssetsProvider


class GameManagerInterface(metaclass=Interface):
    @abstract
    def get_window(self) -> Window:
        pass

    @abstract
    def get_asset_provider(self) -> AssetsProvider:
        pass

    @abstract
    def change_state(self, new_state):
        pass

    @abstract
    def go_to_main_state(self):
        pass
