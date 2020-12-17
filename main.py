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

current_team = Team.WHITE


def calculate_index(row, col):
    return row * 8 + col


def square(x):
    return x * x


def distance_formula(pos1, pos2):
    return math.sqrt(square(pos2[0] - pos1[0]) + square(pos2[1] - pos1[1]))


def nearest_piece(position, listof):
    # TODO refactor this
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

board = [None for _ in range(8 * 8)]

for index, type in enumerate((ChessPieceEnum.ROOK, ChessPieceEnum.KNIGHT, ChessPieceEnum.BISHOP, ChessPieceEnum.QUEEN,
                              ChessPieceEnum.KING, ChessPieceEnum.BISHOP, ChessPieceEnum.KNIGHT, ChessPieceEnum.ROOK)):
    board[calculate_index(0, index)] = type.get_class(pieces_type_image[(type, Team.BLACK)], (0, index), Team.BLACK)

for index in range(8):
    board[calculate_index(1, index)] = Pawn(pieces_type_image[(ChessPieceEnum.PAWN, Team.BLACK)], (1, index), Team.BLACK)

for index in range(8):
    board[calculate_index(6, index)] = Pawn(pieces_type_image[(ChessPieceEnum.PAWN, Team.WHITE)], (6, index), Team.WHITE)

for index, type in enumerate((ChessPieceEnum.ROOK, ChessPieceEnum.KNIGHT, ChessPieceEnum.BISHOP, ChessPieceEnum.QUEEN,
                              ChessPieceEnum.KING, ChessPieceEnum.BISHOP, ChessPieceEnum.KNIGHT, ChessPieceEnum.ROOK)):
    board[calculate_index(7, index)] = type.get_class(pieces_type_image[(type, Team.WHITE)], (7, index), Team.WHITE)

for piece in board:
    if piece is not None:
        pieces_group.add(piece)


def display_possible_moves(display, moves):
    width, height = Settings().get_cell_size()
    print(moves)
    for move in moves:
        row, col = move
        x = col * width + width / 2
        y = row * height + height / 2
        pygame.draw.circle(display, (255, 0, 0), (x, y), 15)


def game_loop(display: pygame.Surface, events: [pygame.event.Event]):
    global selected_piece
    global current_team

    mouse_was_press = False
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_was_press = True

    next_move = None

    if mouse_was_press:
        cursor_position = pygame.mouse.get_pos()
        nearest = nearest_piece(cursor_position, pieces_group)

        if nearest and nearest.belongs_to_team(current_team):
            selected_piece = nearest
        else:
            width, height = Settings().get_cell_size()

            mouse_x, mouse_y = cursor_position
            next_move = (mouse_y // width, mouse_x // height)

    drawboard(display)

    if selected_piece:
        possible_moves = selected_piece.precalculated_moves()

        if next_move:
            if next_move in possible_moves:
                selected_piece.move_to(next_move)
                current_team = Team.BLACK if current_team == Team.WHITE else Team.WHITE
            selected_piece = None
        else:
            display_possible_moves(display, possible_moves)


    pieces_group.draw(display)


window.loop(game_loop)
