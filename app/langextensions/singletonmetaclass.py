"""
This module contains singleton metaclass
"""
from typing import Any


class SingletonMeta(type):
    """
    A metaclass which creates singleton class
    """
    # pyre-ignore[4]:
    _instances = {}

    def __call__(cls, *args: Any, **kwargs: Any):  # pyre-ignore[3]
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
