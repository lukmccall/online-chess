from unittest import TestCase

from game import Window


class TestWindow(TestCase):
    def test_stop_end_loop(self):
        window = Window(1, 1)

        def _loop_stopper(_):
            if _loop_stopper.counter > 1:
                _loop_stopper.fail()
            _loop_stopper.counter += 1
            window.stop()
        _loop_stopper.fail = self.fail
        _loop_stopper.counter = 0

        window.loop(_loop_stopper)

        self.assertEqual(_loop_stopper.counter, 1)

    def test_run_couple_of_times_then_stop(self):
        window = Window(1, 1)

        def _loop_stopper(_):
            if _loop_stopper.counter > 5:
                _loop_stopper.fail()
            _loop_stopper.counter += 1
            if _loop_stopper.counter == 5:
                window.stop()

        _loop_stopper.fail = self.fail
        _loop_stopper.counter = 0

        window.loop(_loop_stopper)

        self.assertEqual(_loop_stopper.counter, 5)
