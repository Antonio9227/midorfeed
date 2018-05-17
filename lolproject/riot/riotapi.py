import requests
import json
from enum import Enum

from champion.models import Champion
from live.models import SummonerSpell

api_key = "RGAPI-bc7651cc-a4ae-4de8-b6ad-f97ce77d3464"
version = "8.10.1"


# Enum for predefined riot api methods
class Method(Enum):
    SummonerByName = "/lol/summoner/v3/summoners/by-name/"  # requires name as param
    GetActiveGame = "/lol/spectator/v3/active-games/by-summoner/"  # requires summoner id
    GetLeague = "/lol/league/v3/positions/by-summoner/"  # requires summoner id
    SummonerById = "/lol/summoner/v3/summoners/"  # requires id as param


# general request function; pass one enum from Method and params
def request(method, param):
    region = "eun1"
    url = "https://" + region + ".api.riotgames.com" + method + param + "?api_key=" + api_key
    r = requests.get(url)
    print(url)
    return json.loads(r.content)


# gets a summoner by summoner name; if the summoner does not exists, it returns -1
def summonerByName(name):
    r = request(Method.SummonerByName.value, name)
    if r.get('status'):
        print("INVALID SUM ID")
        return -1
    return r


# gets a summoner by id
def summonerById(id):
    r = request(Method.SummonerById.value, str(id))
    if r.get('status'):
        return -1
    return r


# returns the game the summoner with that id is in right now or -1
def activeGame(id):
    r = request(Method.GetActiveGame.value, str(id))
    if r.get('status'):
        return -1
    return r


# returns league of specified summoner id
def league(id):
    return request(Method.GetLeague.value, str(id))


# represents an active game participant
class ParticipantDTO:
    def __init__(self, dic):
        self.profileIconId = dic['profileIconId']
        self.championId = dic['championId']
        self.summonerName = dic['summonerName']
        spell1 = SummonerSpell.objects.get(key=int(dic['spell1Id']))
        spell2 = SummonerSpell.objects.get(key=int(dic['spell2Id']))
        self.spell1 = spell1.name
        self.spell2 = spell2.name
        self.spell1Img = spell1.id + ".png"
        self.spell2Img = spell2.id + ".png"
        self.summonerId = dic['summonerId']
        self.teamId = dic['teamId']
        self.focus = 0
        champ = Champion.objects.filter(key=int(dic['championId'])).first()
        if champ:
            self.championName = champ.name
            self.championImage = champ.id + ".png"
        else:
            self.championName = "Unknown?"
            self.championImage = ""


class GameDTO:
    def __init__(self, game):
        self.gameLength = game['gameLength']
