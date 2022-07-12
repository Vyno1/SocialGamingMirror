# views file for weather functionality @Kerstin
from django.http import HttpResponse, JsonResponse
from datetime import date

from .models import WeatherTokens, Player
from .weatherstate import WeatherState
from .kerstin_utils import *


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
    t0 = wt.token0
    t1 = wt.token1
    t2 = wt.token2
    t3 = wt.token3
    t4 = wt.token4
    tfriend = wt.friend_token

    data = {"t0": t0, "t1": t1, "t2": t2, "t3": t3, "t4": t4, "tf": tfriend}
    # data = {"t": [t0, t1, t2, t3, t4], "tf": tfriend}
    # token_string = f'{t0},{t1},{t2},{t3},{t4}#{tfriend}'
    return JsonResponse(data)  # set safe=False to pass any data structure


def load_friend_token(request):
    # TODO: bf = get_best_friend
    # TODO: cw = get_current_weather(bf)
    # TODO: if cw == WeatherTokens.none: -> no daily mark yet (maybe disable button)
    wt: WeatherTokens = get_weather_table(request)
    # TODO: wt.friend_token = cw
    return HttpResponse(success_message)


def get_claim_info(request):
    wt: WeatherTokens = get_weather_table(request)
    # info: #tokens, #friend_tokens, unlocked_friend_token, daily_claimed, current, friends_current
    token_count: int = get_number_of_tokens(wt)
    friend_token_count: int = get_number_of_friend_tokens(wt)
    # TODO: determine if level is high enough
    unlocked_shared_token: bool = False
    daily_claimed: bool = has_claimed_today(wt)
    current = wt.current_weather
    # TODO: get friends' weather
    # MOCK friends weather (simply use own weather)
    friends_current = wt.current_weather  # TODO: change!

    # combine into dict
    data = {"token_count": token_count, "friend_token_count": friend_token_count,
            "unlocked_shared_token": unlocked_shared_token, "daily_claimed": daily_claimed, "current": current,
            "friends_current": friends_current}

    return JsonResponse(data)


# info helpers
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


def has_claimed_today(wt):
    last_update: date = wt.date_of_last_daily_claim
    now: date = date.today()
    return last_update < now
