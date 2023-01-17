from django.conf import settings
from .models.summoner_model import Summoner
import requests
import json
import ast

FIND_SUMMONER_BY_NAME = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{0}"
FIND_SUMMONER_BY_PUUID = "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{0}"
FIND_HISTORY_BY_PUUID = "https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{0}/ids?count={1}"
FIND_MATCH_BY_MATCHID = "https://europe.api.riotgames.com/lol/match/v5/matches/{0}"

class NotFoundException(Exception):
    pass

def get(endpoint):
    http_request = requests.get(endpoint, headers={"X-Riot-Token":settings.RIOT_API})
    if http_request.status_code == 200:
        return http_request.text
    elif http_request.status_code == 404:
        raise NotFoundException()

def get_summoner(name):
    summoner_request = get(FIND_SUMMONER_BY_NAME.format(name))
    return Summoner.from_json(summoner_request)

def get_summoner_by_puuid(name):
    summoner_request = get(FIND_SUMMONER_BY_PUUID.format(name))
    return Summoner.from_json(summoner_request)
    
def get_history(summoner:Summoner, count=20):
    history = get(FIND_HISTORY_BY_PUUID.format(summoner.puuid, str(count)))
    return ast.literal_eval(history)

def get_game(gameid:str):
    return json.loads(get(FIND_MATCH_BY_MATCHID.format(gameid)))
