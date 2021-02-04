from extensions import Interface, abstract
from typing import Optional, Tuple
from .protocol import Message
import socket as soc
import pickle


class SocketWrapperInterface(metaclass=Interface):
    @abstract
    def receive(self) -> Optional[Message]:
        pass

    @abstract
    def send(self, message: Message):
        pass

    @abstract
    def close(self):
        pass


class SocketWrapper(SocketWrapperInterface):
    def __init__(self, socket: soc.socket):
        self.socket = socket

    def receive(self) -> Optional[Message]:
        try:
            encoded_size = self.socket.recv(4, soc.MSG_PEEK)
            if len(encoded_size) == 0:
                raise ConnectionAbortedError("Connection abort")

            if len(encoded_size) != 4:
                return None
            self.socket.recv(4)

            size = int.from_bytes(encoded_size, 'little')
            data = self.socket.recv(size, soc.MSG_PEEK)
            if len(data) != size:
                return None

            self.socket.recv(size)

            return pickle.loads(data)
        except BlockingIOError as e:
            return None

    def send(self, message: Message):
        data = pickle.dumps(message)
        size = len(data)
        encoded_size = size.to_bytes(4, 'little')

        self.socket.send(encoded_size + data)

    def close(self):
        print("close")
        self.socket.close()


class NoneBlockingSocketWrapper(SocketWrapper):
    def __init__(self, socket: soc.socket):
        super().__init__(socket)

        self.socket.setblocking(False)


class ServerSocketWrapper(SocketWrapper):
    def __init__(self, socket: soc.socket):
        super().__init__(socket)

    def bind(self, server_name: str, port: int):
        self.socket.bind((server_name, port))

    def listen(self):
        self.socket.listen()

    def accept(self) -> Tuple[soc.socket, str]:
        return self.socket.accept()
