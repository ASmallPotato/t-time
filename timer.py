from asciimatics.screen import Screen
from datetime import datetime, timedelta

from configparser import ConfigParser

config = ConfigParser(delimiters=('='))
config.read('fonts.ini')
ini_digits = config._sections['digits']

def parse_ini_font(multiline_block, digit):
    return (
        { digit: line }
        for line
        in multiline_block[1:].replace('_', ' ').split('\n')
    )

def merge(dicts):
    return { k: v for d in dicts for k, v in d.items() }

lines_maps = zip(*[
    parse_ini_font(digit, lines)
    for lines, digit
    in ini_digits.items()
])
fonts = [ merge(line_maps) for line_maps in lines_maps ]


def wipe_screen(screen, bg):
    for y in range(screen.height):
        screen._double_buffer[y] = [(" ", bg, 0, bg)] * screen.width
        # for x in range(screen.width):
            # screen._double_buffer[y][x] = (" ", bg, 0, bg)

def get_text_lines(text):
    return ('  '.join(line[c] for c in text) for line in fonts)

def timer(screen, frame_no, timer_config, ev):

    if ev == ord('r') and timer_config.get('r_to_restart', False):
        start_time = datetime.now()
        hours_needed = 0.25
        timer_config['target_time'] = start_time + timedelta(hours=hours_needed, seconds=0)
        wipe_screen(screen, Screen.COLOUR_BLACK)


    def textWidth(offset):
        return (screen.width + offset) // 2 + 1

    now = datetime.now()
    over_time = False

    _micro_sec_diff = (timer_config['target_time'] - now).total_seconds()
    sec_diff = round(_micro_sec_diff)


    if sec_diff < 0:
        over_time = True
        sec_diff = abs(sec_diff)

    min_diff, seconds = divmod(sec_diff, 60)
    hours, minutes = divmod(min_diff, 60)


    new_text = '+' if over_time else ''
    new_text += '{}:'.format(hours) if hours else ''
    new_text += '{:02d}:{:02d}'.format(minutes, seconds)
    # new_text += '{:02d}:{:02d}'.format(hours, minutes)

    y = (screen.height // 2) - 4
    colour = Screen.COLOUR_GREEN
    bg = Screen.COLOUR_BLACK

    if over_time:
        is_odd_frame = _micro_sec_diff % 1 <= 0.5
        bg = Screen.COLOUR_RED if is_odd_frame else Screen.COLOUR_WHITE
        colour = Screen.COLOUR_RED if not is_odd_frame else Screen.COLOUR_WHITE

    wipe_screen(screen, bg)
    for i, line in enumerate(get_text_lines(new_text)):
        screen.print_at(line,
                        textWidth(-len(line)),
                        y + i,
                        colour=colour,
                        bg=bg,
                        transparent=True)

    return 1


if __name__ == '__main__':
    from tui import TUI

    target_time = datetime.now() + timedelta(hours=0, minutes=15, seconds=0)

    timer_args = {
        "target_time": target_time,
        "r_to_restart": True,
    }

    tui = TUI(timer_args, timer)

    tui.start()
