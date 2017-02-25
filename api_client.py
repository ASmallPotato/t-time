from configparser import ConfigParser
from urllib.request import urlopen
import json


config = ConfigParser(delimiters=('='))
config.read('.env.ini')
account_info = config._sections['account']

getUrl = 'https://api.trello.com/1/{{}}?key={api_key}&token={token}&{{}}'.format(**account_info).format



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
