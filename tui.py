from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys
import time


class TUI(object):

    def __init__(self, config, update_function):
        self.frame = 0
        self.update_function = update_function

        self._state = config

    def _main_loop(self, screen):
        while True:
            key_press = screen.get_key()
            signal = self.update_function(
                screen,
                self.frame,
                self._state,
                key_press
            )
            if signal != None:
                return signal
            screen.refresh()
            self.frame += 1
            if not key_press:
                time.sleep(0.25)

    def start(self):
        while True:
            try:
                Screen.wrapper(self._main_loop)
                sys.exit(0)
            except ResizeScreenError:
                pass
            except KeyboardInterrupt:
                sys.exit(0)
