from django.http import HttpResponse
from friends import update_friendship_level


# @Maxi
def get_levels_unlocked(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    return HttpResponse(f"0: {request.player.levels_unlocked}")


# @Maxi
def increase_levels_unlocked(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    player = request.player
    player.levels_unlocked += 1
    player.save()
    return HttpResponse(f"0: {player.levels_unlocked}")


# @Maxi
def get_names(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    if request.user.player.host.count() == 1:
        return HttpResponse(f"0: {request.user.player.host.joined.user.username}")
    else:
        return HttpResponse("1: No Match found")


# @Maxi
def get_match_infos(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
