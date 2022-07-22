from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .models import Player

def getSteps(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    return HttpResponse(f'0: {player.steps}')