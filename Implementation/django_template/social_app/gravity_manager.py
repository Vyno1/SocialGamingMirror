from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import Player
from .models import Match


# @Vyno
def set_start_state(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    object_state: str = request.POST['startState']
    match: Match = request.user.player.joined.all()[0]
    match.gravity_objects = object_state
    match.save()
    return HttpResponse(f'0: successfully set first state')


# @Vyno
def update_object_state(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    object_state: str = request.POST['gravityObjectState']
    match: Match = request.user.player.joined.all()[0]
    match.gravity_objects = object_state
    match.gravity_object_updated = True
    match.save()
    return HttpResponse(f'0: updated gravity object states')


# @Vyno
def send_update_bool(request):
    match: Match = request.user.player.host.all()[0]
    return HttpResponse(f'0: Some Gravity Object has Changed') if match.gravity_object_updated else HttpResponse(
        f'1: No Objects have changed yet')


# @Vyno
def send_object_gravities(request):
    match: Match = request.user.player.host.all()[0]
    match.gravity_object_updated = False
    return HttpResponse(f'0: {match.gravity_objects}')
