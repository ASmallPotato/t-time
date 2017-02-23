from configparser import ConfigParser

config = ConfigParser(delimiters=('='))
config.read('.env.ini')
account_info = config._sections['account']

getUrl = 'https://api.trello.com/1/{{}}?key={api_key}&token={token}&{{}}'.format(**account_info).format






from urllib.request import urlopen
import json


def fromApi(f):
  return json.loads(f.read().decode("utf-8"))

def getLists(boardId):
  with urlopen(getUrl('boards/' + boardId, 'fields=name&lists=open&list_fields=name')) as f:
    return [l for l in fromApi(f)['lists'] if l['name'].startswith('Sprint')]

def getCards(listId):
  with urlopen(getUrl('lists/' + listId, 'fields=name&cards=open&card_fields=name')) as f:
    return fromApi(f)['cards']

lists = getLists('qppTY941')
