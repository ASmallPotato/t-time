from configparser import ConfigParser
from api_client import TrelloBoard, getBoard
from datetime import datetime, timedelta
from timer import timer
from tui import TUI
import re


config = ConfigParser(delimiters=('='))
config.read('t-time.ini')
trello_setting = config._sections['trello']
board_ids = trello_setting['board_ids'].split(',')
visable_trello_list = trello_setting['lists']

_trello_list_matcher = re.compile(visable_trello_list).search


class Storage(object):

    def __init__(self, single_trello_board):
        self.single_trello_board = single_trello_board
        self.trello_board_ids = []
        self.trello_boards = {}
        self.trello_lists = {}
        self.trello_cards = {}

        self.timer = {
            'old_text': None,
            'target_time': None
        }

    def up_sert_trello_boards(self, t_boards):
        self.trello_boards.update(t_boards)

    def up_sert_trello_lists(self, t_lists):
        self.trello_lists.update(t_lists)

    def up_sert_trello_cards(self, cards):
        self.trello_cards.update(cards)




def saveTrelloBoard(app_storage, api_response_board):
    TrelloBoard(
        app_storage,
        api_response_board['id'],
        api_response_board['name'],
        [l for l in api_response_board['lists'] if _trello_list_matcher(l['name'])]
    )



app_storage = Storage(len(board_ids) == 1)

# for board_id in board_ids:
#     saveTrelloBoard(app_storage, getBoard(board_id))





start_time = datetime.now()
hours_needed = 0.002
app_storage.timer['target_time'] = start_time + timedelta(hours=hours_needed, seconds=0)







tui = TUI(app_storage, timer)

tui.start()
