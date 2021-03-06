"""
A module that contains all socket wrappers
"""
import pickle
import socket as soc
from typing import Optional, Tuple

from .protocol import Message
from .socketwrapperinterface import SocketWrapperInterface


class SocketWrapper(SocketWrapperInterface):
    """
    Basic blocking socket wrapper
    """
    def __init__(self, socket: soc.socket) -> None:
        self.socket = socket

    def receive(self) -> Optional[Message]:
        try:
            encoded_size = self.socket.recv(4, soc.MSG_PEEK)
            if len(encoded_size) == 0:
                print("Connection abort")
                raise ConnectionAbortedError("Connection abort")

            if len(encoded_size) != 4:
                return None

            size = int.from_bytes(encoded_size, 'little')
            data = self.socket.recv(4 + size, soc.MSG_PEEK)[4:]
            if len(data) != size:
                return None

            self.socket.recv(4 + size)

            message = pickle.loads(data)
            print("Received {}".format(message))

            return message
        except BlockingIOError:
            return None

    def send(self, message: Message) -> None:
        data = pickle.dumps(message)
        size = len(data)
        encoded_size = size.to_bytes(4, 'little')

        print("Send {}".format(message))
        self.socket.send(encoded_size + data)

    def close(self) -> None:
        self.socket.close()


class NoneBlockingSocketWrapper(SocketWrapper):
    """
    Implementation of non blocking socket wrapper
    """
    def __init__(self, socket: soc.socket) -> None:
        super().__init__(socket)

        self.socket.setblocking(False)


class ServerSocketWrapper(SocketWrapper):
    """
    Extended version of SocketWrapper used by the server
    """
    def bind(self, server_name: str, port: int) -> None:
        """Binds socket to the address

        :param server_name: Ip/name of host
        :param port: Port
        """
        self.socket.bind((server_name, port))

    def listen(self) -> None:
        """Starts listen
        """
        self.socket.listen()

    def accept(self) -> Tuple[soc.socket, str]:
        """Accepts incoming connection
        :return: Socket and address of connected computer
        """
        return self.socket.accept()
