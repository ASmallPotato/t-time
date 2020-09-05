from asciimatics.screen import Screen
from datetime import datetime, timedelta

from configparser import ConfigParser

config = ConfigParser(delimiters=('='))
config.read('fonts.ini')

config_digits_section = config._sections['digits']

font = {
    char: lines_block.replace('_', ' ').split('\n')[1:]
    for char, lines_block
    in config_digits_section.items()
}
line_height = max(len(height) for height in font.values())

def wipe_screen(screen, colour):
    screen._double_buffer = [
        [(" ", colour, 0, colour)] * screen.width
        for y in range(screen.height)
    ]

def get_text_lines(text, letter_spacing=2):
    spacing = ' ' * letter_spacing
    glyphs = (font.get(char) for char in text)
    return (spacing.join(line) for line in zip(*glyphs))

def timer(screen, frame_no, timer_config, ev):
    if ev == ord('q'):
        return 0

    if ev == ord('r') and timer_config.get('r_to_restart', False):
        timer_config['_target_time'] = None
        wipe_screen(screen, Screen.COLOUR_BLACK)

    if '_target_time' not in timer_config:
        start_time = datetime.now()
        timer_config['_target_time'] = start_time + timedelta(**timer_config['duration'])

    def text_width(offset):
        return (screen.width + offset) // 2 + 1

    now = datetime.now()
    is_over_time = False

    micro_sec_diff = (timer_config['_target_time'] - now).total_seconds()
    sec_diff = round(micro_sec_diff)


    if sec_diff < 0:
        is_over_time = True
        sec_diff = abs(sec_diff)

    min_diff, seconds = divmod(sec_diff, 60)
    hours, minutes = divmod(min_diff, 60)


    new_text = '+' if is_over_time else ''
    new_text += '{}:'.format(hours) if hours else ''
    new_text += '{:02d}:{:02d}'.format(minutes, seconds)

    y = (screen.height - line_height) // 2
    colour = Screen.COLOUR_GREEN
    bg = Screen.COLOUR_BLACK

    if is_over_time:
        is_odd_frame = micro_sec_diff % 1 <= 0.5
        if is_odd_frame:
            bg = Screen.COLOUR_RED
            colour = Screen.COLOUR_WHITE
        else:
            bg = Screen.COLOUR_WHITE
            colour = Screen.COLOUR_RED

    wipe_screen(screen, bg)
    for i, line in enumerate(get_text_lines(new_text)):
        screen.print_at(
            line,
            text_width(-len(line)),
            y + i,
            colour=colour,
            bg=bg,
            transparent=True
        )

    return 1


if __name__ == '__main__':
    from tui import TUI

    target_time = datetime.now() + timedelta()

    timer_args = {
        "duration": { "hours": 0, "minutes": 15, "seconds": 0 },
        "r_to_restart": True,
    }

    tui = TUI({ **timer_args }, timer)

    tui.start()
