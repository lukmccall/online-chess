import socket
from _thread import *
import time
import multiplayer as mp
import pickle
from piceces import Team
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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
    connection.send(pickle.dumps(message))


def client(connection, lobby):
    if lobby.is_waiting():
        team = Team.WHITE
        send(connection, mp.SetTeamMessage(Team.WHITE))
    else:
        team = Team.BLACK
        send(connection, mp.SetTeamMessage(Team.BLACK))

    while lobby.is_waiting():
        time.sleep(0.5)

    send(connection, mp.StartMessage())

    other_client = lobby.get_other_client(connection)

    while True:
        if lobby.current_team == team:
            move_message = pickle.loads(connection.recv(1024 * 8))  # type: mp.MoveMessage
            lobby.current_team = Team.WHITE if lobby.current_team == Team.BLACK else Team.BLACK
            other_client.send(pickle.dumps(move_message))

        time.sleep(0.5)


def find_lobby():
    for lobby in lobbies:
        if lobby.is_waiting():
            return lobby
    new_lobby = Lobby()
    lobbies.append(new_lobby)
    return new_lobby


try:
    s.bind((server_name, port))
except socket.error as e:
    print(str(e))

s.listen()
print("Socket start: {}:{}".format(ip, port))
while True:
    connection, address = s.accept()
    print("{} connect".format(address))

    lobby = find_lobby()
    lobby.add_client(connection)

    print(lobbies)
    start_new_thread(client, (connection, lobby))
