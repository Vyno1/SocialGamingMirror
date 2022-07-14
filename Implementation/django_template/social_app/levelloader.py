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
    match = request.user.player.host.all()[0]
    match.current_scene = next_level
    match.sceneChanges = True
    print(player.scene)
    match.save()
    player.save()
    return HttpResponse(f'0: Scene has been updated.')


def get_update(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    match = request.user.player.joined.all()[0]
    match.sceneChanges = False
    player = request.user.player
    player.scene = match.current_scene
    match.save()
    player.save()
    return HttpResponse(f'0: {match.current_scene}')


def ask_for_change(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    match = request.user.player.joined.all()[0]
    if match.sceneChanges:
        return HttpResponse(f'0: scene was changed')
    else:
        return HttpResponse(f'1: scene has not changed yet')


def subtract_steps(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    spent_steps: int = int(request.POST['stepsSpent'])
    print(spent_steps)
    player = request.user.player
    if player.steps >= spent_steps:
        player.steps -= spent_steps
        player.save()
        return HttpResponse(f'0: Steps have been deducted')
    else:
        return HttpResponse(f'1: Not enough steps to be deducted')
