"""
This package contains all state which can be managed by the game manager class
"""
from .stateinterface import StateInterface

from .localgamestate import LocalGameState
from .onlinegamestate import OnlineGameState

from .joininggamestate import JoiningGameState
from .mainmenustate import MainMenuState

from .resultstate import ResultState
