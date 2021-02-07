"""
A base module of the server implementation
"""
from typing import cast
import socket
from _thread import start_new_thread
import time

from constants import Team
from multiplayer import\
    ServerSocketWrapper,\
    NoneBlockingSocketWrapper,\
    LobbyManager, \
    Lobby, \
    SetTeamMessage, \
    StartMessage, \
    MoveMessage, \
    MessageType


def client(connection: socket.socket, lobby: Lobby) -> None:
    """Function which will be run on the client thread.

    :param connection: Client socket
    :param lobby: Lobby with client
    """
    this_connection = NoneBlockingSocketWrapper(connection)

    if lobby.is_waiting():
        team = Team.WHITE
    else:
        team = Team.BLACK

    this_connection.send(SetTeamMessage(team))

    while lobby.is_waiting():
        if lobby.is_close:
            return

        try:
            _ = this_connection.receive()
        except ConnectionAbortedError:
            lobby.close()
            return

        time.sleep(0.1)

    this_connection.send(StartMessage())

    other_client = lobby.get_other_client(connection)
    assert other_client
    other_connection = NoneBlockingSocketWrapper(other_client)

    try:
        while True:
            if lobby.current_team == team:
                message = this_connection.receive()
                if message is None:
                    continue
                if message.type != MessageType.MOVE:
                    continue
                move_message = cast(MoveMessage, message)
                other_connection.send(move_message)
                lobby.current_team = Team.WHITE if lobby.current_team == Team.BLACK else Team.BLACK
            elif lobby.is_close:
                return

            time.sleep(0.1)

    except ConnectionAbortedError:
        pass
    except socket.error as exception:
        print(exception)

    lobby.close()


def main() -> None:
    """Main serve function
    """
    server_name = "localhost"
    port = 5555

    server_socket = ServerSocketWrapper(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

    address = socket.gethostbyname(server_name)

    try:
        server_socket.bind(server_name, port)
    except socket.error as exception:
        print(exception)
        return

    server_socket.listen()
    print("Socket start: {}:{}".format(address, port))

    lobby_manager = LobbyManager()
    try:
        while True:
            connection, address = server_socket.accept()
            print("{} connect".format(address))

            lobby = lobby_manager.find_empty_or_create_new()
            lobby.add_client(connection)

            print(lobby_manager)
            start_new_thread(client, (connection, lobby))
    except KeyboardInterrupt:
        server_socket.close()
        print("Socket closed")


if __name__ == "__main__":
    main()
