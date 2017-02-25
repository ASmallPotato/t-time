from asciimatics.screen import Screen
from datetime import datetime

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




def get_text_lines(text):
    return ('  '.join(line[c] for c in text) for line in fonts)

def timer(screen, frame_no, storage):

    def textWidth(offset):
        return (screen.width + offset) // 2 + 1

    now = datetime.now()
    over_time = False

    _micro_sec_diff = (storage.timer['target_time'] - now).total_seconds()
    sec_diff = round(_micro_sec_diff)


    if sec_diff < 0:
        over_time = True
        sec_diff = abs(sec_diff)

    min_diff, seconds = divmod(sec_diff, 60)
    hours, minutes = divmod(min_diff, 60)


    new_text = '+' if over_time else ''
    # new_text += '{}:'.format(hours) if hours else ''
    new_text += '{:02d}:{:02d}'.format(minutes, seconds)
    # new_text += '{:02d}:{:02d}'.format(hours, minutes)

    bg = Screen.COLOUR_BLACK
    if over_time:
        is_odd_frame = _micro_sec_diff % 1 <= 0.5
        bg = Screen.COLOUR_RED if is_odd_frame else Screen.COLOUR_WHITE

    y = (screen.height // 2) - 4
    colour = Screen.COLOUR_GREEN

    if over_time:
        colour = Screen.COLOUR_RED if not is_odd_frame else Screen.COLOUR_WHITE
        for _y in range(screen.height):
            screen.print_at(" " * screen.width, 0, _y, bg=bg)
    else:
        # Clear old text
        if storage.timer['old_text'] is not None:
            for i, line in enumerate(get_text_lines(storage.timer['old_text'])):
                lineWidth = len(line)
                startX = textWidth(-lineWidth)
                endX = textWidth(+lineWidth)
                screen.move(startX, y + i)
                screen.draw(endX, y + i, char=" ")

    for i, line in enumerate(get_text_lines(new_text)):
        screen.print_at(line,
                              textWidth(-len(line)),
                              y + i,
                              colour=colour,
                              bg=bg,
                              transparent=True)
    storage.timer['old_text'] = new_text

    return 1
