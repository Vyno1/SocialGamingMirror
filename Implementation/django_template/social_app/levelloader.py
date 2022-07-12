from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import Player


def update_level(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    next_level: str = request.POST['nextLevel']
    player = request.user.player
    if next_level == player.scene:
        return HttpResponse(f'1: Scene is already the same!')
    request.user.player.scene = next_level
    match = request.user.player.host.all()
    match.current_scene = next_level
    print(player.scene)
    player.save()
    return HttpResponse(f'0: Scene has been updated.')


def get_update(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    match = request.user.player.host.all()
    request.user.player.scene = match.current_scene
    #test
    return HttpResponse(f'0: {match.current_scene}')
