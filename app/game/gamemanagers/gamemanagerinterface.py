"""
Module containing a GameManagerInterface
"""
from langextensions import Interface, abstract

from ..assets import AssetsProvider
from ..window import Window


class GameManagerInterface(metaclass=Interface):
    """Game manager interface
    """
    @abstract
    def get_window(self) -> Window:
        """Returns current window instance

        :return: Window
        """

    @abstract
    def get_asset_provider(self) -> AssetsProvider:
        """Returns current asset provider

        :return: AssetsProvider
        """

    @abstract
    def change_state(self, new_state) -> None:
        """Changes state and fire state lifecycle methods

         :param new_state: New state of game manager
         """

    @abstract
    def go_to_main_state(self) -> None:
        """Goes to the main menu
        """
