from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .models import Player, Match, WaitingList, Friendship
from .kerstin_utils import *


def addHostLobby(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player

    count = player.waitinghost.all().count()
    if count >= 1:
        response = f'1: Player already in list'
        return HttpResponse(response)
    else:
        WaitingList(waitinghost=player).save()
        response = f'0:'
        return HttpResponse(response)


def findLobby(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    waiters = WaitingList.objects.all()
    print(waiters)
    if waiters.count() >= 1:
        host: Player = waiters[0].waitinghost
        print(host)
        Match(host=host, joined_player=player).save()
        waiters.first().delete()
        return HttpResponse(f'0:' + f'{host.user.username}')
    else:
        return HttpResponse(f'1:')


def wait(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    counter = player.host.all().count()
    if counter >= 1:
        guest: Player = Match.objects.get(host=player).joined_player
        return HttpResponse(f'0:' + f'{guest.user.username}')
    else:
        return HttpResponse(f"1: waitin")


def setJoinedReady(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player

    match: Match = Match.objects.get(joined_player=player)
    match.guest_ready = not match.guest_ready
    match.save()
    if(match.guest_ready):
        return HttpResponse(f'0:')
    else:
        return HttpResponse(f'1:')

def checkJoinedReady(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player

    match: Match = Match.objects.get(host=player)
    if (match.guest_ready):
        return HttpResponse(f'0:')
    else:
        return HttpResponse(f'1:')

def startGame(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    match: Match = Match.objects.get(user__username=player.user.username)
    if match.guest_ready:
        match.has_started = True
        match.save()
        return HttpResponse(f'0:')
    else:
        return HttpResponse(f'lobby not ready')


def leaveLobby(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    waitincount = player.waitinghost.all().count()
    if waitincount >= 1:
        WaitingList.objects.filter(waitinghost=player).delete()
        return HttpResponse(f'0:')
    elif isHostHelper(player):
        match : Match = Match.objects.get(host=player)
        match.host_left = True
        match.save()
    else:
        match: Match = Match.objects.get(joined_player=player)
        match.guest_left = True
        match.save()
    return HttpResponse(f'0:')

def checkIfAlone(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    if isHostHelper(player):
        match: Match = Match.objects.get(host=player)
        if match.guest_left:
            Match.objects.filter(host=player).delete()
            WaitingList(waitinghost=player).save()
            return HttpResponse(f'0:')
        else:
            return HttpResponse(f'1:')
    else:
        match: Match = Match.objects.get(joined_player=player)
        if match.host_left:
            Match.objects.filter(joined_player=player).delete()
            return HttpResponse(f'0:')
        else:
            return HttpResponse(f'1:')



def isHostHelper(player: Player):
    try:
        host : Player = Match.objects.get(host=player).host
        return True
    except ObjectDoesNotExist:
        return False
    #counter = player.host.all().count()
    #if counter >= 1:
    #    return True
    #else:
    #    return False


def isHost(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    count = player.waitinghost.all().count()
    if count >= 1:
        response = f'0:'
        return HttpResponse(response)
    else:
        response = f'1:'
        return HttpResponse(response)

def isFriend(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player = request.user.player
    friend_name = request.POST['name']
    friend = Player.objects.get(user__username=friend_name)
    try:
        friendship = player.friends.get(player2=friend)
    except ObjectDoesNotExist:
        try:
            friendship = player.followers.get(player1=friend)
        except ObjectDoesNotExist:
            return HttpResponse(f'1:')

    return HttpResponse(f'0:')

