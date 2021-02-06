"""
A module containing a socket wrapper interface
"""
from typing import Optional

from langextensions import Interface, abstract

from .protocol import Message


class SocketWrapperInterface(metaclass=Interface):
    """
    Common interface of socket wrappers
    """
    @abstract
    def receive(self) -> Optional[Message]:
        """Receives data from underlying socket

        :return: Message is available or None
        :raise ConnectionAbortedError: if connection was closed
        """

    @abstract
    def send(self, message: Message) -> None:
        """Sends data to underlying socket

        :param message: Message to send
        """

    @abstract
    def close(self) -> None:
        """Closes the underlying connection
        """
