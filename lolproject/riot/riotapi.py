import requests
import json
from enum import Enum

api_key = "RGAPI-1d3636d6-a561-46ee-8211-8747de5d05a1"


# Enum for predefined riot api methods
class Method(Enum):
    SummonerByName = "/lol/summoner/v3/summoners/by-name/"  # requires name as param
    GetActiveGame = "/lol/spectator/v3/active-games/by-summoner/"  # requires summoner id


# general request function; pass one enum from Method and params
def request(method, param):
    region = "eun1"
    url = "https://" + region + ".api.riotgames.com" + method + param + "?api_key=" + api_key
    r = requests.get(url)
    print(url)
    return json.loads(r.content)


# gets a summoner by summoner name; if the summoner does not exists, it returns id -1
def summonerByName(name):
    r = request(Method.SummonerByName.value, name)
    if r.get('status'):
        return {'id': -1}
    return r


def activeGame(id):
    r = request(Method.GetActiveGame.value, str(id))
    if r.get('status'):
        return {'id': -1}
    return r
