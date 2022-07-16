# views file of @Kerstin
from django.http import HttpResponse

from .models import Player, Match
from .kerstin_utils import *


# -------------------------------------------------{ get match helper }-------------------------------------------------

def get_match(request):
    if request.method != 'POST' or not hasattr(request.user, 'player'):
        return None

    player: Player = request.user.player
    # you can "|" filters for performing an "OR" sql query
    match = Match.objects.filter(host=player) | Match.objects.filter(joined_player=player)

    if not match:
        return None

    # filter returns a "QuerySet" = ~ List of entities -> take first
    return match.first()


# ----------------------------------------------------{ Pause Game }----------------------------------------------------

def pause_game(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    if match.is_paused:
        return HttpResponse(failed_message)

    match.is_paused = True
    return HttpResponse(success_message)


def get_paused(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    if match.is_paused:
        return HttpResponse(bool_true)
    return HttpResponse(bool_false)


# ---------------------------------------------------{ Pause Buttons }--------------------------------------------------

def resume_game(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    if not match.is_paused:
        return HttpResponse(f'1: game is not paused')

    match.is_paused = False
    return HttpResponse(success_message)


def reset_game(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    if match.do_reset:
        return HttpResponse('1: reset already requested')

    match.do_reset = True
    return HttpResponse(success_message)


def exit_game(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    if match.do_exit:
        return HttpResponse('1: exit already requested')

    match.do_reset = True
    return HttpResponse(success_message)


# ------------------------------------------------------{ Getters }-----------------------------------------------------

def get_reset(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    if match.do_reset:
        return HttpResponse(bool_true)

    return HttpResponse(bool_false)


def get_exit(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    if match.do_exit:
        return HttpResponse(bool_true)

    return HttpResponse(bool_false)

# --------------------------------------------------------{ END }-------------------------------------------------------
