from django.urls import path

from . import views


app_name = 'lol'
urlpatterns = [
    path('', views.IndexView, name='index'),
    path('summoner', views.SummonerView, name='summoner'),
    path('lastgame', views.LastGameView, name='lastgame'),
    path('laststat', views.LastGameStats, name='laststat'),

]