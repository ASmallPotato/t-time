from random import choice
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.effects import Effect
from asciimatics.exceptions import ResizeScreenError
import sys
from datetime import datetime, timedelta

from configparser import ConfigParser

config = ConfigParser(delimiters=('='))
config.read('fonts.ini')
iniDigits = config._sections['digits']

def parseIniFont(multilineBlock, key):
    return ({key: line} for line in multilineBlock[1:].replace('_', ' ').split('\n'))

def merge(dicts):
    return {k: v for d in dicts for k, v in d.items()}

fonts = [merge(dicts) for dicts in zip(*[parseIniFont(v, k) for k, v in iniDigits.items()])]
fontHeights = len(fonts)




# seconds_spent = 0;

start_time = datetime.now() # - timedelta(hours=3)


hours_needed = 0.001

seconds_needed = hours_needed * 360

target_time = start_time + timedelta(hours=hours_needed)





class MainLoop(Effect):
    def __init__(self, screen, bg=Screen.COLOUR_BLACK, **kwargs):
        """
        :param screen: The Screen being used for the Scene.
        """
        super(MainLoop, self).__init__(**kwargs)
        self._screen = screen
        self._bg = bg
        self._old_text = None

    def reset(self):
        pass

    def _update(self, frame_no):
        def getTextLines(text):
            return ('  '.join(line[c] for c in text) for line in fonts)

        def textWidth(offset):
            return (self._screen.width + offset) // 2 + 1

        y = (self._screen.height // 2) - 4


        now = datetime.now()
        over_time = False

        sec_diff = round((target_time - now).total_seconds())


        if sec_diff < 0:
            over_time = True
            sec_diff = abs(sec_diff)

        min_diff, seconds = divmod(sec_diff, 60)
        hours, minutes = divmod(min_diff, 60)


        # Clear old text
        if self._old_text is not None:
            for i, line in enumerate(getTextLines(self._old_text)):
                lineWidth = len(line)
                startX = textWidth(-lineWidth)
                endX = textWidth(+lineWidth)
                self._screen.move(startX, y + i)
                self._screen.draw(endX, y + i, char=" ")


        new_text = '+' if over_time else ''
        # new_text += '{}:'.format(hours) if hours else ''
        # new_text += '{:02d}:{:02d}'.format(minutes, seconds)
        new_text += '{:02d}:{:02d}'.format(hours, minutes)

        for i, line in enumerate(getTextLines(new_text)):
            self._screen.print_at(line,
                                  textWidth(-len(line)),
                                  y + i,
                                  colour=Screen.COLOUR_GREEN,
                                  bg=self._bg,
                                  # bg=Screen.COLOUR_WHITE,
                                  transparent=True)
        self._old_text = new_text

    @property
    def stop_frame(self):
        return self._stop_frame

    @property
    def frame_update_count(self):
        # Only need to update once a second
        # return 20
        return 10













def demo(screen):

    scenes = []
    effects = [
        MainLoop(screen)
    ]
    scenes.append(Scene(effects, -1))
    screen.play(scenes, stop_on_resize=True)

while True:
    try:
        Screen.wrapper(demo)
        sys.exit(0)
    except ResizeScreenError:
        pass
