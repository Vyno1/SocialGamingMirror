# views file of @Kerstin
from django.http import HttpResponse, JsonResponse

from .models import Player, Match
from .kerstin_utils import *

# -------------------------------------------------{ get match helper }-------------------------------------------------
from .weatherstate import WeatherState


def get_match(request):
    if not hasattr(request.user, 'player'):
        return None

    player: Player = request.user.player

    player_is_host: bool = player.host.all().count() == 1
    match: Match = Match.objects.get(host=player) if player_is_host else Match.objects.get(joined_player=player)

    if not match:
        return None

    return match


# ----------------------------------------------------{ Pause Game }----------------------------------------------------

def pause_game(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse("There is no such match")

    if match.is_paused:
        return HttpResponse("already paused")

    match.is_paused = True
    match.save()

    return HttpResponse(success_message)


def resume_game(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    if not match.is_paused:
        return HttpResponse('1: game is not paused')

    match.is_paused = False
    match.save()

    return HttpResponse(success_message)


def get_paused(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    if match.is_paused:
        return HttpResponse("0")
    return HttpResponse("1")


# ---------------------------------------------------{ Level Tokens }---------------------------------------------------

def get_level_tokens(request) -> JsonResponse:
    match: Match = get_match(request)

    if not match:
        # safe=False so that Json doesn't have to return a dict
        return JsonResponse(failed_message, safe=False)

    t1 = match.host_token
    t2 = match.joined_token

    data: dict = {"t1": t1, "t2": t2}

    return JsonResponse(data)


def set_level_tokens(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    match.host_token = request.POST['t1']
    match.joined_token = request.POST['t2']

    return HttpResponse(success_message)


def get_host_token(request) -> HttpResponse:
    # print("get host was requested by " + request.user.username)

    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    return HttpResponse(str(match.host_token))


def get_joined_token(request) -> HttpResponse:
    # print("get joined was requested by " + request.user.username)

    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    return HttpResponse(str(match.joined_token))


def set_host_token(request) -> HttpResponse:
    print("set host was requested by " + request.user.username)

    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    state: str = request.POST['weather']
    match.host_token = string_2_weatherstate(state)

    match.save()

    return HttpResponse(success_message)


def set_joined_token(request) -> HttpResponse:
    print("set joined was requested by " + request.user.username)

    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    state: str = request.POST['weather']
    match.joined_token = string_2_weatherstate(state)

    match.save()

    return HttpResponse(success_message)


# -----------------------------------------------{ string to weatherstate }---------------------------------------------

def string_2_weatherstate(string: str) -> WeatherState:
    if string == "sun":
        return WeatherState.sun
    if string == "rain":
        return WeatherState.sun
    if string == "snow":
        return WeatherState.snow
    if string == "wind":
        return WeatherState.wind
    if string == "thunder":
        return WeatherState.thunder

    print(string)
    return WeatherState.none

# --------------------------------------------------------{ END }-------------------------------------------------------
