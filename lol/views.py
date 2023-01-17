from django.shortcuts import render
from django.conf import settings
from .riot_models import *
import requests
import json

# Create your views here.

def IndexView(request):
    template_name = 'index.html'
    return render(request, template_name)


def SummonerView(request):
    template_name = 'summoner.html'
    summoner = None
    if request.method == "POST":
        
        summoner = requests.get(
            "https://euw1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" + request.POST.get("summoner"),
             headers={"X-Riot-Token":settings.RIOT_API})
        
        if summoner.status_code == 200:
            summoner = Summoner(** json.loads(summoner.text))
            print(summoner.name)

    data = {"summoner": summoner}
    return render(request, template_name, data)
        