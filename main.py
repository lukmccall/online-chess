import pygame

from piceces import *
from settings import Settings
from spritesheet import SpriteSheet
from window import Window
import math

window = Window(*Settings().get_window_size())

light_brown = (251, 196, 117)
dark_brown = (139, 69, 0)

colors = (light_brown, dark_brown)

selected_piece = None

pieces_group = pygame.sprite.Group()


def calculate_index(row, col):
    return row * 8 + col


def square(x):
    return x * x


def distance_formula(pos1, pos2):
    return math.sqrt(square(pos2[0] - pos1[0]) + square(pos2[1] - pos1[1]))


def nearest_piece(position, listof):
    nearest = None
    posCounter = 50000  # a very high number/ could use board dimension^2
    for piece in listof:
        if distance_formula(piece.rect.center, position) < posCounter:
            nearest = piece
            posCounter = distance_formula(piece.rect.center, position)
    if posCounter < Settings().get_window_size()[1] / 8 - 30:
        return nearest  # only works when close
    else:
        return None


def drawboard(diplay: pygame.Surface):
    width, height = Settings().get_window_size()
    width, height = width // 8, height // 8
    index = 1  # toswitchcolors (index - 1) * -1
    for column in range(8):
        for row in range(8):
            cell = pygame.Rect(row * height, column * width, width + 1, height + 1)
            pygame.draw.rect(diplay, colors[index], cell)
            index = (index - 1) * -1
        index = (index - 1) * -1


ss = SpriteSheet("assets/chess-pieces-sprite.png")
images = ss.images(2, 6)

pieces = pygame.sprite.Group()

piece_num = 0
pieces_type_image = {}

for color in ('white', 'black'):
    for piece_type in (
            ChessPieceEnum.KING,
            ChessPieceEnum.QUEEN,
            ChessPieceEnum.BISHOP,
            ChessPieceEnum.KNIGHT,
            ChessPieceEnum.ROOK,
            ChessPieceEnum.PAWN):
        pieces_type_image[(piece_type, color)] = images[piece_num]
        piece_num += 1

board = [None for _ in range(8 * 8)]

for index, type in enumerate((ChessPieceEnum.ROOK, ChessPieceEnum.KNIGHT, ChessPieceEnum.BISHOP, ChessPieceEnum.QUEEN,
                              ChessPieceEnum.KING, ChessPieceEnum.BISHOP, ChessPieceEnum.KNIGHT, ChessPieceEnum.ROOK)):
    board[calculate_index(0, index)] = type.get_class(pieces_type_image[(type, 'black')], (0, index), 0)

for index in range(8):
    board[calculate_index(1, index)] = Pawn(pieces_type_image[(ChessPieceEnum.PAWN, 'black')], (1, index), 0)

for index in range(8):
    board[calculate_index(6, index)] = Pawn(pieces_type_image[(ChessPieceEnum.PAWN, 'white')], (6, index), 0)

for index, type in enumerate((ChessPieceEnum.ROOK, ChessPieceEnum.KNIGHT, ChessPieceEnum.BISHOP, ChessPieceEnum.QUEEN,
                              ChessPieceEnum.KING, ChessPieceEnum.BISHOP, ChessPieceEnum.KNIGHT, ChessPieceEnum.ROOK)):
    board[calculate_index(7, index)] = type.get_class(pieces_type_image[(type, 'white')], (7, index), 0)

for piece in board:
    if piece is not None:
        pieces_group.add(piece)


def game_loop(display: pygame.Surface, events: [pygame.event.Event]):
    drawboard(display)

    mouse_was_press = False
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_was_press = True

    if mouse_was_press:
        cursor_position = pygame.mouse.get_pos()
        nearest = nearest_piece(cursor_position, pieces_group)
        print(nearest)

    pieces_group.draw(display)

window.loop(game_loop)
