from unittest import TestCase, mock
import pygame

from game import GameController


class TestGameController(TestCase):
    def test_pipe_events(self):
        # noinspection PyTypeChecker
        game_controller = GameController(None, None)
        event = pygame.event.Event(pygame.MOUSEBUTTONUP)

        self.assertFalse(game_controller._mouse_was_press)

        game_controller.pipe_events([event])

        self.assertTrue(game_controller._mouse_was_press)

    @mock.patch("game.boards.GameBoardInterface")
    @mock.patch("pygame.mouse.get_pos", return_value=(5, 6))
    def test__get_mouse_index(self, mocked_pygame_mouse_pos, mocked_game_board_class):
        game_board = mocked_game_board_class.return_value
        game_board.get_cell_size.return_value = (1, 1)

        # noinspection PyTypeChecker
        game_controller = GameController(game_board, None)
        mouse_index = game_controller._get_mouse_index()

        mocked_pygame_mouse_pos.assert_called_once()
        game_board.get_cell_size.assert_called_once()
        self.assertEqual(mouse_index, (6, 5))
