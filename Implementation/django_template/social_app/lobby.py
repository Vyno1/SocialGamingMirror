from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from .models import Player, Match, Friendship
from .kerstin_utils import *


def checkIfHost(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player = request.user.player
    try:
        Match.objects.get(host=player, )
        return HttpResponse(f'0:')
    except ObjectDoesNotExist:
        return HttpResponse(f'1:')
    except Exception as e:
        print(e)
        return HttpResponse(f'1:')



def addHostLobby(request):
    if request.method != 'POST':
        return HttpResponse(wrong_method_message)
    if not hasattr(request.user, 'player'):
        return HttpResponse(not_a_player_message)

    player: Player = request.user.player
    if not Match.waiting_list.contains(player):
        Match.waiting_list.add(player)
        return HttpResponse(f'0:')
    else:
        return HttpResponse(f'user already in HostLobby')

def findLobby(request):
    if request.method != 'POST':
        return HttpResponse(wrong_method_message)
    if not hasattr(request.user, 'player'):
        return HttpResponse(not_a_player_message)

    player: Player = request.user.player
    if Match.waiting_list.count() == 0:
        return HttpResponse(f'no lobby found')
    else:
        createMatch(Match.waiting_list.first(), player)
        return HttpResponse(f'0:')


def createMatch(host: Player, joined: Player):
    Match.joined_player = joined
    Match.host = host
    Match.waiting_list.remove(Match.waiting_list.first())

def startGame(request):
    if request.method != 'POST':
        return HttpResponse(wrong_method_message)
    if not hasattr(request.user, 'player'):
        return HttpResponse(not_a_player_message)

    player: Player = request.user.player
    match: Match = Match.objects.get(user__username=player.user.username)
    if match.guest_ready:
        match.has_started = True
        return HttpResponse(f'0:')
    else:
        return HttpResponse(f'lobby not ready')


def checkIfFriend(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    friend_name = request.POST['name']
    friend = Player.objects.get(user__username=friend_name)
    player = request.user.player
    response = f'0:'
    try:
        friendship = Friendship.objects.get(player=player, friend=friend)
        if friendship.mutual is True:
            response+= ''
        else:
            response += f", no friendship"
    except ObjectDoesNotExist:
        response += f", no friendship"
        Friendship(player=player, friend=friend).save()
    except Exception as e:
        print(e)
        response += f", something went wrong, nothing changed."

    return HttpResponse(response)