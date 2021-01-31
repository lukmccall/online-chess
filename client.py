from piceces import *
from engine import Board, MultiplayerGameController
from settings import Settings
from spritesheet import SpriteSheet
from window import Window

import socket
import pickle
import multiplayer as mp

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 5555))

team_message = pickle.loads(s.recv(1024 * 8))  # type: mp.SetTeamMessage
my_team = team_message.team

window = Window(*Settings().get_window_size())

light_brown = (251, 196, 117)
dark_brown = (139, 69, 0)

colors = (light_brown, dark_brown)

pieces_group = pygame.sprite.Group()

current_team = Team.WHITE

ss = SpriteSheet("assets/chess-pieces-sprite.png")
images = ss.images(2, 6)

pieces = pygame.sprite.Group()

piece_num = 0
pieces_type_image = {}

for team in (Team.WHITE, Team.BLACK):
    for piece_type in (
            ChessPieceEnum.KING,
            ChessPieceEnum.QUEEN,
            ChessPieceEnum.BISHOP,
            ChessPieceEnum.KNIGHT,
            ChessPieceEnum.ROOK,
            ChessPieceEnum.PAWN):
        pieces_type_image[(piece_type, team)] = images[piece_num]
        piece_num += 1

b = Board(window.game_display, pieces_type_image)

game_controller = MultiplayerGameController(b, my_team, s)

start_message = pickle.loads(s.recv(1024 * 8))  # type: mp.StartMessage
s.setblocking(False)

def game_loop(display: pygame.Surface, events: [pygame.event.Event]):
    b.draw()
    if b.is_game_over():
        window.is_running = False
        print("koniec")
        return

    game_controller.pipe_events(events)

    game_controller.action()


window.loop(game_loop)
