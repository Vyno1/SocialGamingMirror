from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import Player
from .models import Match
from .lobby import isHostHelper


def check_if_already_collected_host(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    level_number: int = int(request.POST['levelNumber'])
    player: Player = request.user.player
    if player.host.all().count() != 1:
        return HttpResponse("Nonono")
    match: Match = request.user.player.host.all()[0]
    collected: str = player.collection
    if collected[level_number - 1] == '1':
        match.level_collectable_already_collected = True
        match.save()
        return HttpResponse(f'1: Collectable was already collected')
    else:
        return HttpResponse(f'0: Collectable has not been collected')


def check_if_already_collected_joined(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    player: Player = request.user.player
    if isHostHelper(player):
        match: Match = request.user.player.host.all()[0]
    else:
        match: Match = request.user.player.joined.all()[0]
    if match.level_collectable_already_collected:
        match.level_collectable_already_collected = False
        match.save()
        return HttpResponse(f'1: Collectable was already collected')
    else:
        return HttpResponse(f'0: Collectable has not been collected')


def update_collection(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    level_number: int = int(request.POST['levelNumber'])
    player: Player = request.user.player
    if isHostHelper(player):
        collection: str = player.collection
        player.collection = collection[:level_number - 1] + '1' + collection[level_number:]
        player.number_collected += 1
        print(collection)
        match: Match = request.user.player.host.all()[0]
        match.level_collectable_already_collected = True
        match.save()
        player.save()
        return HttpResponse(f'0: Updated collection')
    else:
        host: Player = Match.objects.get(joined_player=player).host
        collection: str = host.collection
        host.collection = collection[:level_number - 1] + '1' + collection[level_number:]
        host.number_collected += 1
        match: Match = request.user.player.joined.all()[0]
        match.level_collectable_already_collected = True
        match.save()
        print(collection)
        host.save()
        return HttpResponse(f'0: Updated collection for host')

def getCollectables(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    player: Player = request.user.player

    return HttpResponse(f'0: {player.number_collected}')
