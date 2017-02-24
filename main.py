from configparser import ConfigParser

config = ConfigParser(delimiters=('='))
config.read('.env.ini')
account_info = config._sections['account']

getUrl = 'https://api.trello.com/1/{{}}?key={api_key}&token={token}&{{}}'.format(**account_info).format




# config = ConfigParser(delimiters=('='))
config.read('t-time.ini')
trello_setting = config._sections['trello']
board_ids = trello_setting['board_ids'].split(',')
visable_trello_list = trello_setting['lists']


import re

_trello_list_matcher = re.compile(visable_trello_list).search



from urllib.request import urlopen
import json


def fromApi(f):
  return json.loads(f.read().decode("utf-8"))

def getBoard(boardId):
  with urlopen(getUrl('boards/' + boardId, 'fields=name&lists=open&list_fields=name')) as f:
    return fromApi(f)

def getLists(boardId):
  with urlopen(getUrl('boards/' + boardId, 'fields=name&lists=open&list_fields=name')) as f:
    return [l for l in fromApi(f)['lists'] if _trello_list_matcher(l['name'])]

def getCards(listId):
  with urlopen(getUrl('lists/' + listId, 'fields=name&cards=open&card_fields=name')) as f:
    return fromApi(f)['cards']




class Storage(object):

    def __init__(self, single_trello_board):
        self.single_trello_board = single_trello_board
        self.trello_board_ids = []
        self.trello_boards = {}
        self.trello_lists = {}
        self.trello_cards = {}

    def up_sert_trello_boards(self, t_boards):
        self.trello_boards.update(t_boards)

    def up_sert_trello_lists(self, t_lists):
        self.trello_lists.update(t_lists)

    def up_sert_trello_cards(self, cards):
        self.trello_cards.update(cards)

class TrelloCard(object):

    def __init__(self, app_storage, id, name):
        self._app_storage = app_storage

        self.id = id
        self.name = name

        self._app_storage.up_sert_trello_cards({self.id: self})


class TrelloList(object):

    def __init__(self, app_storage, id, name, t_cards):
        self._app_storage = app_storage

        self.id = id
        self.name = name

        for t_card in t_cards:
            TrelloList(app_storage, t_card['id'], t_card['name'])
        self.t_cards = [t_card['id'] for t_card in t_cards]
        self._app_storage.up_sert_trello_lists({self.id: self})

class TrelloBoard(object):

    def __init__(self, app_storage, id, name, t_lists):
        self._app_storage = app_storage

        self.id = id
        self.name = name

        for t_list in t_lists:
            TrelloList(app_storage, t_list['id'], t_list['name'], [])
        self.t_lists = [t_list['id'] for t_list in t_lists]

        if not self.id in self._app_storage.trello_boards:
            self._app_storage.trello_board_ids += [self.id]
        self._app_storage.up_sert_trello_boards({self.id: self})



def saveTrelloBoard(app_storage, api_response_board):
    TrelloBoard(
        app_storage,
        api_response_board['id'],
        api_response_board['name'],
        [l for l in api_response_board['lists'] if _trello_list_matcher(l['name'])]
    )



app_storage = Storage(len(board_ids) == 1)

for board_id in board_ids:
    saveTrelloBoard(app_storage, getBoard(board_id))
