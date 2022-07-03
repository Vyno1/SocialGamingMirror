# views file for weather functionality @Kerstin
from django.db import models
from django.http import HttpResponse

from .models import WeatherTokens, Player
from .kerstin_utils import *


# choices is django's equivalent of enums
class WeatherState(models.TextChoices):
    sun = 'sun'
    rain = 'rain'
    wind = 'wind'
    thunder = 'thunder'
    snow = 'snow'
    none = 'none'


def get_weather_table(request):
    if request.method != 'POST':
        return HttpResponse(wrong_method_message)
    if not hasattr(request.user, 'player'):
        return HttpResponse(not_a_player_message)

    player: Player = request.user.player

    # sql query
    wt = WeatherTokens.objects.filter(owner__user_id=player.id)
    if not wt:
        return HttpResponse(no_match_message)

    return wt.first()


def set_current_weather(request):
    wt: WeatherTokens = get_weather_table(request)
    wt.current_weather = request.POST['current_weather']
    return HttpResponse(success_message)


def get_current_weather(player: Player):
    wt = WeatherTokens.objects.filter(owner_id=player)
    cw = wt.first().current_weather
    return cw


def get_tokens(request):
    wt: WeatherTokens = get_weather_table(request)
    # build string; "t0,t1,...,t4#tfriend"
    t0 = wt.token0
    t1 = wt.token1
    t2 = wt.token2
    t3 = wt.token3
    t4 = wt.token4
    tfriend = wt.friend_token
    token_string = f'{t0},{t1},{t2},{t3},{t4}#{tfriend}'
    return HttpResponse("0: " + token_string)


def load_friend_token(request):
    # TODO: bf = get_best_friend
    # TODO: cw = get_current_weather(bf)
    # TODO: if cw == WeatherTokens.none: -> no daily mark yet (maybe disable button)
    wt: WeatherTokens = get_weather_table(request)
    # TODO: wt.friend_token = cw
    return HttpResponse(success_message)

