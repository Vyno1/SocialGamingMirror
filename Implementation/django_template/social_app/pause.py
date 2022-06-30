# views file of @Kerstin
from django.http import HttpResponse

from .models import Player, Match

not_signed_in_message = '1: user not signed in'
wrong_method_message = '1: incorrect request method'
not_a_player_message = '1: user is not a player'
no_match_message = '1: user has no match'

success_message = '0: success'
bool_true = '0'
bool_false = '1'


# helper function
def get_match(request):
    # if not request.user.is_authenticated:
    #     return HttpResponse(not_signed_in_message)
    if request.method != 'POST':
        return HttpResponse(wrong_method_message)
    if not hasattr(request.user, 'player'):
        return HttpResponse(not_a_player_message)

    player: Player = request.user.player
    # TODO: check if this detects both host and joined player (otherwise adjust joined_player attribute in DB)
    if not hasattr(player, 'match'):
        return HttpResponse(no_match_message)

    match: Match = player.match
    return match


def pause_game(request):
    """sets is_paused in match = true, failure if already true"""
    match: Match = get_match(request)

    if match.is_paused:
        return HttpResponse(f'1: game is already paused')

    match.is_paused = True
    return HttpResponse(success_message)


def get_paused(request):
    """queries is_paused in match and returns it"""
    match: Match = get_match(request)
    # TODO: exchange by using resp dictionary

    if match.is_paused:
        return HttpResponse(bool_true)
    return HttpResponse(bool_false)


def resume_game(request):
    """sets is_paused in match = false, failure if already false"""

    match: Match = get_match(request)
    if not match.is_paused:
        return HttpResponse(f'1: game is not paused')

    match.is_paused = False
    return HttpResponse(success_message)


def request_reset(request):
    """sets do_reset in match = true, failure if already true"""

    match: Match = get_match(request)
    if match.do_reset:
        return HttpResponse('1: reset already requested')

    match.do_reset = True
    return HttpResponse(success_message)


# reset level is unnecessary, Unity writes updated game state attributes after reset


def request_exit(request):
    """sets do_exit in match = true, failure if already true"""

    match: Match = get_match(request)
    if match.do_exit:
        return HttpResponse('1: exit already requested')

    match.do_reset = True
    return HttpResponse(success_message)

# TODO: clear db after level? exit?
