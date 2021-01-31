from piceces import *
from engine import Board, GameController
from settings import Settings
from spritesheet import SpriteSheet
from window import Window

window = Window(*Settings().get_window_size())

light_brown = (251, 196, 117)
dark_brown = (139, 69, 0)

colors = (light_brown, dark_brown)

pieces_group = pygame.sprite.Group()

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



white_controller, black_controller = GameController(b, Team.WHITE), GameController(b, Team.BLACK)


def game_loop(display: pygame.Surface, events: [pygame.event.Event]):
    if b.turn() == Team.WHITE:
        game_controller = white_controller
    else:
        game_controller = black_controller

    b.draw()
    if b.is_game_over():
        window.is_running = False
        print("koniec")
        return

    game_controller.pipe_events(events)

    game_controller.action()


window.loop(game_loop)
