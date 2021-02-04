from typing import Optional

from langextensions import Interface, abstract

from .protocol import Message


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
