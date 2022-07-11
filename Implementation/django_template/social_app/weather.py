# views file for weather functionality @Kerstin
from django.http import HttpResponse, JsonResponse
from datetime import date

from .models import WeatherTokens, Player
from .weatherstate import WeatherState
from .kerstin_utils import *


# ---------------------------------------------------{ Get and Set }----------------------------------------------------

def get_weather_table(request):
    if not hasattr(request.user, 'player'):
        return None  # HttpResponse(not_a_player_message)

    player: Player = request.user.player

    # sql query
    wt = WeatherTokens.objects.get(owner=player)
    # print("owner of wt: " + wt.__str__())
    return wt


# works :)
def set_current_weather(request) -> HttpResponse:
    wt: WeatherTokens = get_weather_table(request)

    wt.current_weather = request.POST['current']
    wt.save()

    return HttpResponse(success_message)


def get_current_weather(player: Player) -> WeatherState:
    wt = WeatherTokens.objects.get(owner=player)
    return wt.current_weather


def get_tokens_dict(request) -> dict:
    wt: WeatherTokens = get_weather_table(request)

    t0 = wt.token0
    t1 = wt.token1
    t2 = wt.token2
    t3 = wt.token3
    t4 = wt.token4
    tfriend = wt.friend_token

    data = {"t0": t0, "t1": t1, "t2": t2, "t3": t3, "t4": t4, "tf": tfriend}

    return data  # set safe=False to pass any data structure


# --------------------------------------------------{ Weather Updates }-------------------------------------------------

# every change in tokens... has to be registered here!
def update_player_weather(request) -> HttpResponse:
    wt: WeatherTokens = get_weather_table(request)

    if wt is None:
        return HttpResponse(failed_message)

    # store in db
    wt.token0 = request.POST['t0']
    wt.token1 = request.POST['t1']
    wt.token2 = request.POST['t2']
    wt.token3 = request.POST['t3']
    wt.token4 = request.POST['t4']

    # wt.friend_token = request.POST['tf']

    if request.POST['update_daily'] == "true":
        wt.date_of_last_daily_claim = date.today()

    return HttpResponse(success_message)


# --------------------------------------------------{ Get Claim Info }--------------------------------------------------

def load_tokens(request) -> JsonResponse:
    wt: WeatherTokens = get_weather_table(request)

    if wt is None:
        data: dict = {"success": 1}
        return JsonResponse(data, safe=False)

    # info: daily_claimed, all tokens

    claimed: bool = has_claimed_today(wt)
    tokens: dict = get_tokens_dict(request)

    # TODO: determine if level is high enough
    # unlocked_shared_token: bool = False

    # TODO: get friends' weather
    # MOCK friends weather (simply use own weather)
    # friends_current = wt.current_weather  # TODO: change!

    # | merges 2 dictionaries (if x is contained in both, it takes x from right dict)
    data: dict = {"claimed": claimed} | tokens
    return JsonResponse(data)


# ------------------------------------------------{ Claim Info Helpers }------------------------------------------------

def get_number_of_tokens(wt: WeatherTokens):
    count = 0
    # a token is counted if it has a state
    if not wt.token0 == WeatherState.none:
        count += 1
    if not wt.token1 == WeatherState.none:
        count += 1
    if not wt.token2 == WeatherState.none:
        count += 1
    if not wt.token3 == WeatherState.none:
        count += 1
    if not wt.token4 == WeatherState.none:
        count += 1
    return count


def get_number_of_friend_tokens(wt: WeatherTokens):
    if wt.friend_token == WeatherState.none:
        return 0
    return 1


def has_claimed_today(wt: WeatherTokens):
    last_update: date = wt.date_of_last_daily_claim
    now: date = date.today()
    claimed: bool = last_update >= now
    return claimed


def load_friend_token(request):
    # TODO: bf = get_best_friend
    # TODO: cw = get_current_weather(bf)
    # TODO: if cw == WeatherTokens.none: -> no daily mark yet (maybe disable button)
    wt: WeatherTokens = get_weather_table(request)

    if wt is None:
        return HttpResponse(failed_message)

    # TODO: wt.friend_token = cw
    return HttpResponse(success_message)
