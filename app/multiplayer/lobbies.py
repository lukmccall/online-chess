"""
This module contains LobbyManager and Lobby
"""
from __future__ import annotations
from typing import List, Optional, Iterator
import socket
from threading import Lock
import itertools

from constants import Team


class LobbyManager:
    """
    A class that managing a lobby - provides simple methods to handle all needed lobby actions
    """
    def __init__(self) -> None:
        self._lobbies: List[Lobby] = []

    def create_lobby(self) -> Lobby:
        """Creates new lobby

        :return: A new lobby
        """
        new_lobby = Lobby(self)
        self._lobbies.append(new_lobby)
        return new_lobby

    def remove_lobby(self, lobby: Lobby) -> None:
        """Removes lobby from manager inner list

        :param lobby: Lobby to remove
        """
        self._lobbies.remove(lobby)

    def find_empty_or_create_new(self) -> Lobby:
        """Finds a empty lobby or if not exit creates a new one

        :return: Lobby
        """
        for lobby in self._lobbies:
            if lobby.is_waiting():
                return lobby

        return self.create_lobby()

    def __str__(self) -> str:
        lobbies = "\n".join([str(lobby) for lobby in self._lobbies])
        return "Lobby manager:\n{}".format(lobbies)


class Lobby:
    """
    Simple container which holds references to all clients which are playing together
    """

    ID: Iterator[int] = itertools.count()

    def __init__(self, lobby_manager: LobbyManager) -> None:
        self._id: int = next(self.ID)
        self._lobby_manager: LobbyManager = lobby_manager
        self._clients: List[socket.socket] = []
        self.current_team: Team = Team.WHITE
        self._is_close: bool = False
        self._lock: Lock = Lock()

    def add_client(self, client: socket.socket) -> None:
        """Adds client to the lobby

        :param client: Client socket
        """
        self._clients.append(client)

    def is_empty(self) -> bool:
        """Checks if the lobby is empty

        :return: whatever the lobby is empty
        """
        return len(self) == 0

    def is_waiting(self) -> bool:
        """Checks if the lobby needs more player to start

        :return: whatever the lobby needs more player
        """
        return len(self) != 2

    def __len__(self) -> int:
        return len(self._clients)

    def get_other_client(self, client: socket.socket) -> Optional[socket.socket]:
        """Gets other client socket

        :param client: Client socket
        :return: Other client
        """
        for other_clients in self._clients:
            if other_clients is not client:
                return other_clients
        return None

    @property
    def is_close(self) -> bool:
        """Checks if the lobby is closed

        :return: whatever the lobby is closed
        """
        return self._is_close

    def close(self) -> None:
        """Closes the lobby and remove it from the manager
        """
        self._lock.acquire()
        if self._is_close:
            self._lock.release()
            return

        for client in self._clients:
            try:
                client.close()
            except (OSError, socket.error) as exception:
                print(exception)

        self._is_close = True
        self._lobby_manager.remove_lobby(self)
        self._lock.release()

    def __str__(self) -> str:
        return "Lobby #{} with {} players.".format(self._id, len(self))
