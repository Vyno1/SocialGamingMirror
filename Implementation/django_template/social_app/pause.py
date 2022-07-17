# views file of @Kerstin
from django.http import HttpResponse

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

# --------------------------------------------------------{ END }-------------------------------------------------------
