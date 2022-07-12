from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .models import Player, Match, WaitingList
from .kerstin_utils import *


def addHostLobby(request):
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


def findLobby(request):
    if request.method != 'POST':
        return HttpResponse(wrong_method_message)
    if not hasattr(request.user, 'player'):
        return HttpResponse(not_a_player_message)

    player: Player = request.user.player
    waiters = WaitingList.objects.all()
    print(waiters)
    if waiters.count() >= 1:
        host: Player = waiters[0].waitinghost
        print(host)
        Match(host=host, joined_player=player).save()
        host.delete()
        return HttpResponse(f'0:' + f'{host.user.username}')
    else:
        return HttpResponse(f'1:')


def wait(request):
    if request.method != 'POST':
        return HttpResponse(wrong_method_message)
    if not hasattr(request.user, 'player'):
        return HttpResponse(not_a_player_message)

    player: Player = request.user.player

    try:
        guest: Player = Match.objects.get(host=player).joined_player
        return HttpResponse(f'0:' + f'{guest.user.username}')
    except:
        return HttpResponse(f"1: waitin")


def setJoinedReady(request):
    if request.method != 'POST':
        return HttpResponse(wrong_method_message)
    if not hasattr(request.user, 'player'):
        return HttpResponse(not_a_player_message)

    player: Player = request.user.player

    match: Match = Match.objects.get(joined_player=player)
    match.guest_ready = True
    match.save()
    return HttpResponse(f'0:')


def startGame(request):
    if request.method != 'POST':
        return HttpResponse(wrong_method_message)
    if not hasattr(request.user, 'player'):
        return HttpResponse(not_a_player_message)

    player: Player = request.user.player
    match: Match = Match.objects.get(user__username=player.user.username)
    if match.guest_ready:
        match.has_started = True
        match.save()
        return HttpResponse(f'0:')
    else:
        return HttpResponse(f'lobby not ready')


def leaveLobby(request):
    if request.method != 'POST':
        return HttpResponse(wrong_method_message)
    if not hasattr(request.user, 'player'):
        return HttpResponse(not_a_player_message)

    player: Player = request.user.player

    if (isHost(player)):
        try:
            wait = WaitingList.objects.get(waitinghost=player)
            wait.delete()
            return HttpResponse(f"0: left WaitingQueque")
        except ObjectDoesNotExist:
            match: Match = Match.objects.get(host=player)
            match.delete()
            return HttpResponse(f"0: Host left Lobby -> match deleted")
    else:
        match: Match = Match.objects.get(joined_player=player)
        WaitingList(waitinghost=match.host)
        Match.objects.filter(joined_player=player).delete()
        return HttpResponse(f"1: Joined Player left lobby -> host in waitinglist")


def isHost(player: Player):
    try:
        Match.objects.get(host=player)
        return True
    except ObjectDoesNotExist:
        return False


def isHost(request):
    if request.method != 'POST':
        return HttpResponse(wrong_method_message)
    if not hasattr(request.user, 'player'):
        return HttpResponse(not_a_player_message)

    player: Player = request.user.player
    count = player.host.all().count()
    if count >= 1:
        WaitingList.objects.get(player)
        return HttpResponse(f'0:')
    else:
        return HttpResponse(f'1:')

# def checkIfFriend(request):
#    if not request.user.is_authenticated:
#        return HttpResponse(f'user not signed in')
#    if request.method != 'GET':
#        return HttpResponse(f'incorrect request method.')
#    if not hasattr(request.user, 'player'):
#        return HttpResponse(f'user is not a player')
#
#    player: Player = request.user.player
#    friend: Player = Match.objects.get(player)
#    try:
#        friendship = player.friends.get(player2=friend)
#    except ObjectDoesNotExist:
#        try:
#            friendship = player.followers.get(player1=friend)
#        except ObjectDoesNotExist as error:
#            print(f"No mutual friendship between \"{player.user.username}\" and \"{friend.user.username}\"!")
#            print(error)
#            friendship = None
