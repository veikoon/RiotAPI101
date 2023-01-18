from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models.summoner_model import Summoner
from .utils import *
import requests
import json
import ast

# Create your views here.

def IndexView(request):
    template_name = 'index.html'
    return render(request, template_name)


def SummonerView(request):
    template_name = 'summoner.html'
    summoner = None
    if request.method == "POST":
        try:
            summoner = get_summoner(request.POST.get("summoner"))
            request.session["summoner"] = summoner.to_json()
        except NotFoundException:
            messages.warning(request, "Impossible de trouver le joueur " + request.POST.get("summoner"))

        return HttpResponseRedirect(request.path_info)

    if "summoner" in request.session:
            summoner = Summoner.from_json(request.session["summoner"])

    data = {"summoner": summoner}
    return render(request, template_name, data)


def LastGameView(request):
    template_name = 'game.html'

    if not "summoner" in request.session:
        redirect("lol:summoner")
    
    summoner = Summoner.from_json(request.session["summoner"])

    try:
        last_game_id = get_history(summoner, 1)[0]
        last_game = get_game(last_game_id)
    except NotFoundException:
        messages.warning(request, "Impossible de trouver la dernière partie")
        redirect("lol:index")
    
    summoners_team1 = []
    summoners_team2 = []
    for summoner_info in last_game["info"]["participants"]:
        if summoner_info["teamId"] == 100:
            summoners_team1.append({
                "summonerName": summoner_info["summonerName"],
                "summonerLevel": summoner_info["summonerLevel"],
                "championName": summoner_info["championName"],
            })
        else:
            summoners_team2.append({
                "summonerName": summoner_info["summonerName"],
                "summonerLevel": summoner_info["summonerLevel"],
                "championName": summoner_info["championName"],
            })


    data = {"summoners_team1": summoners_team1, "summoners_team2": summoners_team2}
    return render(request, template_name, data)


def LastGameStats(request):
    template_name = 'personnal_stat.html'

    if not "summoner" in request.session:
        redirect("lol:summoner")
    
    summoner = Summoner.from_json(request.session["summoner"])

    try:
        last_game_id = get_history(summoner, 1)[0]
        last_game = get_game(last_game_id)
    except NotFoundException:
        messages.warning(request, "Impossible de trouver la dernière partie")
        redirect("lol:index")

    stats = {}
    perks = {}
    challenges = {}
    for summoner_info in last_game["info"]["participants"]:
        if summoner_info["summonerName"] == summoner.name:
            for summoner_stat in summoner_info:
                if summoner_stat in ["perks", "challenges"]:
                    continue
                else:
                    stats[summoner_stat] = summoner_info[summoner_stat]
            
            for challenges_stat in summoner_info["challenges"]:
                challenges[challenges_stat] = summoner_info["challenges"][challenges_stat]

    # Vision
    pings = {}
    champion = {}
    visions = {}
    spells = {}
    try:
        pings["Basic"] = [stats["basicPings"], "img/ping/generic.png"]
        pings["Danger"] = [stats["dangerPings"], "img/ping/danger.png"]
        pings["On My Way"] = [stats["onMyWayPings"], "img/ping/onmyway.png"]
        pings["Missing"] = [stats["enemyMissingPings"], "img/ping/missing.png"]
        pings["Assist me"] = [stats["assistMePings"], "img/ping/assistme.png"]
        pings["All In"] = [stats["allInPings"], "img/ping/allin.png"]
        pings["Push"] = [stats["pushPings"], "img/ping/push.png"]
        pings["Bait"] = [stats["baitPings"], "img/ping/bait.png"]
        pings["Caution"] = [stats["getBackPings"], "img/ping/caution.png"]
        pings["Push"] = [stats["pushPings"], "img/ping/push.png"]
        pings["Hold"] = [stats["holdPings"], "img/ping/hold.png"]
        pings["Command"] = [stats["commandPings"], "img/ping/command.jpg"]
        pings["Need Vision"] = [stats["needVisionPings"], "img/ping/needvision.png"]
        pings["Ennemy Vision"] = [stats["enemyVisionPings"], "img/ping/ennemyvision.png"]
        pings["Cleared Vision"] = [stats["visionClearedPings"], "img/ping/visioncleared.png"]

        visions["Wards Detected"] = [stats["detectorWardsPlaced"], "img/ping/wardsdetected.png"]
        visions["Wards Placed"] = [stats["wardsPlaced"], "assets/dragontail/13.1.1/img/item/3340.png"]
        visions["Wards Destroyed"] = [stats["wardsKilled"], "assets/dragontail/13.1.1/img/item/3364.png"]
        visions["Control Wards Purchased"] = [challenges["controlWardsPlaced"], "assets/dragontail/13.1.1/img/item/2055.png"]

        champion["champExperience"] = stats["champExperience"]
        champion["champLevel"] = stats["champLevel"]
        champion["championName"] = stats["championName"]
        champion["kills"] = stats["kills"]
        champion["assists"] = stats["assists"]
        champion["deaths"] = stats["deaths"]

        f = open('static/assets/dragontail/13.1.1/data/fr_FR/champion/' + stats["championName"] + '.json')
        champion_data = json.load(f)
        spell1 = champion_data["data"][stats["championName"]]["spells"][0]["name"]
        spell2 = champion_data["data"][stats["championName"]]["spells"][1]["name"]
        spell3 = champion_data["data"][stats["championName"]]["spells"][2]["name"]
        spell4 = champion_data["data"][stats["championName"]]["spells"][3]["name"]

        spells[spell1] = [stats["spell1Casts"], "assets/dragontail/13.1.1/img/spell/" + stats["championName"]  + "Q.png"]
        spells[spell2] = [stats["spell2Casts"], "assets/dragontail/13.1.1/img/spell/" + stats["championName"]  + "W.png"]
        spells[spell3] = [stats["spell3Casts"], "assets/dragontail/13.1.1/img/spell/" + stats["championName"]  + "E.png"]
        spells[spell4] = [stats["spell4Casts"], "assets/dragontail/13.1.1/img/spell/" + stats["championName"]  + "R.png"]
        champion["spells"] = spells


    except ValueError:
        messages.error(request, "Erreur interne : " + ValueError)

    data = {
        "stats": stats,
        "challenges": challenges,
        "pings": pings,
        "visions": visions,
        "champion": champion,
        }
    return render(request, template_name, data)

        