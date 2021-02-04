from engine import GameController, MultiplayerGameController, Board, Settings
from extensions import Interface, abstract
from piceces import Team
from window import Window
import pygame_menu
import pygame
import chess
from multiplayer import SocketWrapperInterface, NoneBlockingSocketWrapper, MessageType
import socket


class GameStateInterface(metaclass=Interface):
    @abstract
    def on_state_exit(self):
        pass

    @abstract
    def on_state_start(self):
        pass

    @abstract
    def on_game_loop(self, display: pygame.surface.Surface, events: [pygame.event.Event]):
        pass


class GameManager:
    def __init__(self, window: Window, asset_provider):
        self.window = window
        self.asset_provider = asset_provider

        self.state = MainMenuState(self)
        self.state.on_state_start()

    def game_loop(self, display: pygame.surface.Surface, events: [pygame.event.Event]):
        for event in events:
            if event.type == pygame.QUIT:
                self.window.is_running = False
                self.state.on_state_exit()
                return
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.change_state(MainMenuState(self))
                return
        try:
            self.state.on_game_loop(display, events)
        except Exception as e:
            print(e)
            self.change_state(MainMenuState(self))

    def change_state(self, new_state: GameStateInterface):
        print("change stata")
        self.state.on_state_exit()
        self.state = new_state
        self.state.on_state_start()


class MainMenuState(GameStateInterface):
    def __init__(self, game_manager: GameManager):
        self.game_manager = game_manager

        self.menu = pygame_menu.Menu(
            game_manager.window.height,
            game_manager.window.width,
            "Online Chess",
            theme=pygame_menu.themes.THEME_DARK,
            enabled=False
        )

        self.menu.add_button("Play", self.on_new_local_game)
        self.menu.add_button("Multiplayer", self.on_multiplayer_game)
        self.menu.add_vertical_margin(20)
        self.menu.add_selector(
            "Flip board",
            [("No", False), ("Yes", True)],
            default=1 if Settings().get_flip_board() else 0,
            onchange=lambda _, to: Settings().set_flip_board(to)
        )
        self.menu.add_vertical_margin(20)
        self.menu.add_button("Quit", self.on_end)

    def on_state_exit(self):
        self.menu.disable()

    def on_state_start(self):
        self.menu.enable()

    def on_game_loop(self, display: pygame.surface.Surface, events: [pygame.event.Event]):
        if self.menu.is_enabled():
            self.menu.update(events)
            if not self.menu.is_enabled():
                return
            self.menu.draw(self.game_manager.window.game_display)

    def on_new_local_game(self):
        self.game_manager.change_state(LocalGameState(self.game_manager))

    def on_end(self):
        self.game_manager.window.is_running = False

    def on_multiplayer_game(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", 5555))
        except ConnectionRefusedError as e:
            print(e)
            return
        self.game_manager.change_state(JoiningGameState(self.game_manager, NoneBlockingSocketWrapper(s)))


class ResultState(GameStateInterface):
    def __init__(self, game_manager: GameManager, board):
        self.game_manager = game_manager
        self.board = board
        self.font = pygame.font.Font(pygame.font.get_default_font(), 70)

        self.result = self._get_result()

    def _get_result(self):
        color = self.board.winner()

        if color is None:
            text = "Draw"
        elif color == chess.WHITE:
            text = "White win"
        else:
            text = "Black win"

        return text

    def on_state_exit(self):
        pass

    def on_state_start(self):
        pass

    def draw_game_result(self):
        text = self.font.render(self.result, True, Settings().get_text_color())

        text_position = self.game_manager.window.width / 2 - text.get_width() / 2, self.game_manager.window.height / 2 - text.get_height() / 2
        pygame.draw.rect(self.game_manager.window.game_display, (0, 0, 0), pygame.Rect(text_position[0] - 20, text_position[1] - 10, text.get_width() + 40, text.get_height() + 15))
        self.game_manager.window.game_display.blit(text, text_position)

    def on_game_loop(self, display: pygame.surface.Surface, events: [pygame.event.Event]):
        for event in events:
            if event.type == pygame.KEYDOWN:
                self.game_manager.change_state(MainMenuState(self.game_manager))
                return

        self.board.draw()
        self.draw_game_result()


class LocalGameState(GameStateInterface):
    def __init__(self, game_manger: GameManager):
        self.game_manager = game_manger
        self.white_controller = None
        self.black_controller = None
        self.board = None

    def on_state_exit(self):
        pass

    def on_state_start(self):
        self.board = Board(self.game_manager.window.game_display, self.game_manager.asset_provider.get_pieces_factory())
        self.white_controller = GameController(self.board, Team.WHITE)
        self.black_controller = GameController(self.board, Team.BLACK)

    def on_game_loop(self, display: pygame.surface.Surface, events: [pygame.event.Event]):
        if self.board.turn() == Team.WHITE:
            game_controller = self.white_controller
        else:
            game_controller = self.black_controller

        game_controller.prepare()

        self.board.draw()

        if self.board.is_game_over():
            self.game_manager.change_state(ResultState(self.game_manager, self.board))
            return

        game_controller.pipe_events(events)
        game_controller.action()


class JoiningGameState(GameStateInterface):
    def __init__(self, game_manager: GameManager, socket: SocketWrapperInterface):
        self.game_manager = game_manager
        self.socket = socket

        self.menu = pygame_menu.Menu(
            game_manager.window.height,
            game_manager.window.width,
            "Online Chess",
            theme=pygame_menu.themes.THEME_DARK,
            enabled=False
        )

        self.menu.add_label("Waiting for connection")
        self.menu.add_button("Quit", self.on_end)

        self.preserve_socket = False
        self.team = None

    def on_state_exit(self):
        self.menu.disable()

        if not self.preserve_socket:
            self.socket.close()

    def on_state_start(self):
        self.menu.enable()

    def on_game_loop(self, display: pygame.surface.Surface, events: [pygame.event.Event]):
        if self.menu.is_enabled():
            self.menu.update(events)
            if not self.menu.is_enabled():
                return
            self.menu.draw(self.game_manager.window.game_display)

        message = self.socket.receive()
        if message is None:
            return

        if self.team is None:
            if message.type == MessageType.SET_TEAM:
                self.team = message.team
            else:
                raise AssertionError("Expect [SET_TEAM] message but got {}.".format(message))
        else:
            if message.type == MessageType.START:
                self.preserve_socket = True
                self.game_manager.change_state(OnlineGameState(self.game_manager, self.socket, self.team))
            else:
                raise AssertionError("Expect [START] message but got {}.".format(message))

    def on_end(self):
        self.game_manager.change_state(MainMenuState(self.game_manager))


class OnlineGameState(GameStateInterface):
    def __init__(self, game_manager: GameManager, socket: SocketWrapperInterface, team: Team):
        self.game_manager = game_manager
        self.socket = socket
        self.team = team

        self.game_controller = None
        self.board = None

    def on_state_exit(self):
        self.socket.close()

    def on_state_start(self):
        self.board = Board(
            self.game_manager.window.game_display,
            self.game_manager.asset_provider.get_pieces_factory()
        )

        self.game_controller = MultiplayerGameController(self.board, self.team, self.socket)

    def on_game_loop(self, display: pygame.surface.Surface, events: [pygame.event.Event]):
        self.board.draw()

        if self.board.is_game_over():
            self.game_manager.change_state(ResultState(self.game_manager, self.board))
            return

        self.game_controller.pipe_events(events)
        self.game_controller.action()

