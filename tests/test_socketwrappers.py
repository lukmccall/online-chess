from unittest import TestCase, mock
import socket as soc
import pickle

from multiplayer import \
    SocketWrapper, \
    NoneBlockingSocketWrapper, \
    ServerSocketWrapper, \
    StartMessage, \
    Message, \
    MessageType

data = pickle.dumps(StartMessage())
size_of_data = len(data)
encoded_size = size_of_data.to_bytes(4, 'little')
correct_encoded_message = encoded_size + data


def recv_stub_creator(buffer):
    def stub(size, flag=None):
        if stub.buffer is None:
            raise BlockingIOError()
        to_return = stub.buffer[:size]

        if flag is not None:
            if flag != soc.MSG_PEEK:
                raise NotImplementedError()

            return to_return

        stub.buffer = stub.buffer[size:]
        return to_return

    stub.buffer = buffer
    return stub


@mock.patch("socket.socket")
class TestSocketWrapper(TestCase):
    def test_receive_throws_on_connection_close(self, mocked_socket_class):
        mocked_socket = mocked_socket_class.return_value
        mocked_socket.recv.side_effect = recv_stub_creator(b"")

        try:
            socket = SocketWrapper(mocked_socket)
            socket.receive()
            self.fail()
        except ConnectionAbortedError:
            pass

    def test_receive_gets_correct_message(self, mocked_socket_class):
        mocked_socket = mocked_socket_class.return_value
        mocked_socket.recv.side_effect = recv_stub_creator(correct_encoded_message)

        socket = SocketWrapper(mocked_socket)
        message = socket.receive()

        self.assertIsNotNone(message)
        self.assertIsInstance(message, Message)
        self.assertEqual(message.type, MessageType.START)
        mocked_socket.recv.assert_called_with(len(correct_encoded_message))

    def test_not_consume_buffer_if_message_is_not_ready(self, mocked_socket_class):
        recv_stub = recv_stub_creator(encoded_size)
        mocked_socket = mocked_socket_class.return_value
        mocked_socket.recv.side_effect = recv_stub
        socket = SocketWrapper(mocked_socket)
        message = socket.receive()

        self.assertIsNone(message)
        self.assertTrue(len(recv_stub.buffer) > 0)
        self.assertListEqual(list(recv_stub.buffer), list(encoded_size))

    def test_not_consume_buffer_if_message_is_not_fully_loaded(self, mocked_socket_class):
        recv_stub = recv_stub_creator(correct_encoded_message[:-5])
        mocked_socket = mocked_socket_class.return_value
        mocked_socket.recv.side_effect = recv_stub
        socket = SocketWrapper(mocked_socket)
        message = socket.receive()

        self.assertIsNone(message)
        self.assertTrue(len(recv_stub.buffer) > 0)
        self.assertListEqual(list(recv_stub.buffer), list(correct_encoded_message[:-5]))

    def test_close(self, mocked_socket_class):
        mocked_socket = mocked_socket_class.return_value

        socket = SocketWrapper(mocked_socket)
        socket.close()

        mocked_socket.close.assert_called_once()

    def test_send(self, mocked_socket_class):
        mocked_socket = mocked_socket_class.return_value

        socket = SocketWrapper(mocked_socket)
        socket.send(StartMessage())

        mocked_socket.send.assert_called_with(correct_encoded_message)


@mock.patch("socket.socket")
class TestNoneBlockingSocketWrapper(TestCase):
    def test_check_if_none_blocking(self, mocked_socket_class):
        mocked_socket = mocked_socket_class.return_value

        NoneBlockingSocketWrapper(mocked_socket)

        mocked_socket.setblocking.assert_called_with(False)


@mock.patch("socket.socket")
class TestServerSocketWrapper(TestCase):
    def test_bind(self, mocked_socket_class):
        mocked_socket = mocked_socket_class.return_value

        server_socket = ServerSocketWrapper(mocked_socket)
        server_socket.bind("test", 123)

        mocked_socket.bind.assert_called_with(("test", 123))

    def test_listen(self, mocked_socket_class):
        mocked_socket = mocked_socket_class.return_value

        server_socket = ServerSocketWrapper(mocked_socket)
        server_socket.listen()

        mocked_socket.bind.asser_called_once()

    def test_accept(self, mocked_socket_class):
        mocked_socket = mocked_socket_class.return_value
        connected_socket_obj = object()
        mocked_socket.accept.return_value = (connected_socket_obj, "test")

        server_socket = ServerSocketWrapper(mocked_socket)
        connected_socket, address = server_socket.accept()

        mocked_socket.accept.asser_called_once()
        self.assertEqual(connected_socket, connected_socket_obj)
        self.assertEqual(address, "test")
