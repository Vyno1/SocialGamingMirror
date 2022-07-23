from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import Player
from .models import Match
from .lobby import isHostHelper


# @Vyno
def update_object_state(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    object_state: str = request.POST['buttonObjectState']
    player: Player = request.user.player
    if isHostHelper(player):
        match: Match = request.user.player.host.all()[0]
        match.button_object_updated_from_host = True
    else:
        match: Match = request.user.player.joined.all()[0]
        match.button_object_updated_from_join = True
    match.button_objects = object_state
    match.save()
    return HttpResponse(f'0: updated button object states')


def send_update_bool(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    player: Player = request.user.player
    if isHostHelper(player):
        match: Match = request.user.player.host.all()[0]
        return HttpResponse(f'0: A Button has changed') if match.button_object_updated_from_join else HttpResponse(
            f'1: No Button has changed')
    else:
        match: Match = request.user.player.joined.all()[0]
        return HttpResponse(f'0: A Button has changed') if match.button_object_updated_from_host else HttpResponse(
            f'1: No Button has changed')


def send_button_states(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    player: Player = request.user.player
    if isHostHelper(player):
        match: Match = request.user.player.host.all()[0]
        match.button_object_updated_from_join = False
    else:
        match: Match = request.user.player.joined.all()[0]
        match.button_object_updated_from_host = False
    match.save()
    return HttpResponse(f'0: {match.button_objects}')
