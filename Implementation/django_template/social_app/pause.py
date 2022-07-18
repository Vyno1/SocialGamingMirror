# views file of @Kerstin
from django.http import HttpResponse, JsonResponse

from .models import Player, Match
from .kerstin_utils import *


# -------------------------------------------------{ get match helper }-------------------------------------------------

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

    t1 = match.token1
    t2 = match.token2

    data: dict = {"t1": t1, "t2": t2}

    return JsonResponse(data)


def set_level_tokens(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    match.token1 = request.POST['t1']
    match.token2 = request.POST['t2']

    return HttpResponse(success_message)

# --------------------------------------------------------{ END }-------------------------------------------------------
