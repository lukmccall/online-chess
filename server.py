import socket
from _thread import *
import time
from typing import Optional

import multiplayer as mp
import pickle
from piceces import Team
from multiplayer import ServerSocketWrapper, SocketWrapper

server_socket = ServerSocketWrapper(socket.socket(socket.AF_INET, socket.SOCK_STREAM))

server_name = "localhost"
port = 5555

ip = socket.gethostbyname(server_name)

lobbies = []


class Lobby:
    def __init__(self):
        self.clients = []
        self.current_team = Team.WHITE

    def add_client(self, connection):
        self.clients.append(connection)

    def is_empty(self):
        return len(self) == 0

    def is_waiting(self):
        return len(self) != 2

    def __len__(self):
        return len(self.clients)

    def get_other_client(self, connection):
        for client in self.clients:
            if client is not connection:
                return client
        return None



def send(connection, message: mp.Message):
    bytes = pickle.dumps(message)
    size = len(bytes)
    encoded = size.to_bytes(4, 'little')
    connection.send(encoded + bytes)


def client(connection, lobby):
    this_connection = SocketWrapper(connection)

    if lobby.is_waiting():
        team = Team.WHITE
    else:
        team = Team.BLACK

    this_connection.send(mp.SetTeamMessage(team))

    while lobby.is_waiting():
        time.sleep(0.5)

    send(connection, mp.StartMessage())

    other_client = lobby.get_other_client(connection)
    other_connection = SocketWrapper(other_client)

    while True:
        if lobby.current_team == team:
            move_message = this_connection.receive()  # type: Optional[mp.MoveMessage]
            if move_message is None:
                continue
            lobby.current_team = Team.WHITE if lobby.current_team == Team.BLACK else Team.BLACK
            other_connection.send(move_message)

        time.sleep(0.5)


def find_lobby():
    for lobby in lobbies:
        if lobby.is_waiting():
            return lobby
    new_lobby = Lobby()
    lobbies.append(new_lobby)
    return new_lobby


try:
    server_socket.bind(server_name, port)
except socket.error as e:
    print(str(e))

server_socket.listen()

print("Socket start: {}:{}".format(ip, port))
while True:
    connection, address = server_socket.accept()
    print("{} connect".format(address))

    lobby = find_lobby()
    lobby.add_client(connection)

    print(lobbies)
    start_new_thread(client, (connection, lobby))
