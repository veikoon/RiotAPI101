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

    data = {"stats": stats, "challenges": challenges}
    return render(request, template_name, data)

        