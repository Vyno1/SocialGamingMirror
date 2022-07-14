# views file for weather functionality @Kerstin
from django.http import HttpResponse, JsonResponse
from datetime import date

from .models import WeatherTokens, Player

from .weatherstate import WeatherState
from .kerstin_utils import *
from .friends import get_best_friend


# --------------------------------------------------{ Create Table }----------------------------------------------------

def create_weather_table(request):
    if not hasattr(request.user, 'player'):
        print("no such player!")
        return None

    player: Player = request.user.player

    # other attributes have correct default value
    WeatherTokens.objects.create(owner=player)

    return HttpResponse(success_message)


# ---------------------------------------------------{ Get and Set }----------------------------------------------------

def get_weather_table(request):
    if not hasattr(request.user, 'player'):
        return None  # HttpResponse(not_a_player_message)

    player: Player = request.user.player
    print(player)

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

    data = {"t0": t0, "t1": t1, "t2": t2, "t3": t3, "t4": t4}

    return data


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

    if request.POST['update_daily'] == bool_true:
        wt.date_of_last_daily_claim = date.today()

    if request.POST['used_shared'] == bool_true:
        wt.used_shared = True

    wt.save()

    return HttpResponse(success_message)


# -------------------------------------------------{ Get Weather Info }-------------------------------------------------

def load_tokens(request) -> JsonResponse:
    wt: WeatherTokens = get_weather_table(request)

    if wt is None:
        data: dict = {"success": 1}
        return JsonResponse(data, safe=False)

    # gather weather information for response
    claimed: bool = has_claimed_today(wt)
    tokens: dict = get_tokens_dict(request)

    unlocked_shared: bool = has_unlocked_shared(player=request.user.player)
    best_friend: str = "vyno1"  # get_friend_name()
    friends_current: WeatherState = WeatherState.none

    if unlocked_shared and not wt.used_shared:
        friends_current = load_friend_token(request)

    # | merges 2 dictionaries (if x is contained in both, it takes x from right dict)
    data: dict = tokens | {"claimed": claimed, "unlocked_shared": unlocked_shared, "best_friend": best_friend,
                           "tf": friends_current}
    return JsonResponse(data)


# -----------------------------------------------{ Weather Info Helpers }-----------------------------------------------

def has_claimed_today(wt: WeatherTokens):
    last_update: date = wt.date_of_last_daily_claim
    now: date = date.today()
    claimed: bool = last_update >= now
    return claimed


# -----------------------------------------------{ Shared Token Helpers }-----------------------------------------------

def get_friend_name(player: Player) -> str:
    return player.user.username


def has_unlocked_shared(player) -> bool:
    bf: Player = get_best_friend(player)
    return bf is None


def load_friend_token(request) -> WeatherState:
    bf: Player = get_best_friend(request.user.player)

    # None means you sadly have no good friends
    if bf is None:
        return WeatherState.none

    cw: WeatherState = get_current_weather(bf)
    return cw
