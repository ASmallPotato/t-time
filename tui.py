from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError
import sys
import time


class TUI(object):

    def __init__(self, storage, update_function):
        self.frame = 0
        self.update_function = update_function

        self._storage = storage

    def _main_loop(self, screen):
        while True:
            ev = screen.get_key()
            sig = self.update_function(screen, self.frame, self._storage, ev)
            if not sig:
                return
            screen.refresh()
            self.frame += 1
            if not ev:
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
