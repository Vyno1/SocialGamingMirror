from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .models import Player, Match, WaitingList, InviteMatch, Walk2Gether, Friendship

def getSteps(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    return HttpResponse(f'0: {player.steps}')

def setSteps(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player = request.user.player
    steps = request.POST['steps']
    player.steps = steps
    player.save()
    return HttpResponse(f'0:')

def sendCoords(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player = request.user.player
    coordsX = request.POST['coordsX']
    coordsY = request.POST['coordsY']
    player.coordinates = coordsX + "/" + coordsY
    player.save()
    return HttpResponse(f'0:')

def getFriendSteps(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player = request.user.player
    friendName = request.POST['friend']
    friend = Player.objects.get(user__username=friendName)
    coords = friend.coordinates
    if(coords == "0"):
        return HttpResponse(f'1:')
    return HttpResponse(f'0:' + f'{coords}')



def inviteFriendWalk(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player = request.user.player
    friend_name = request.POST['name']
    friend = Player.objects.get(user__username=friend_name)
    print(friend.coordinates)
    if friend.coordinates == "0":
        # friend not in stepScene
        return HttpResponse(f'1:')
    else:
        Walk2Gether(player1=player, player2=friend).save()
        return HttpResponse(f'0:')

def checkIfInvitedWalk(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player : Player = request.user.player
    count = player.playerTwo.all().count()
    if count > 0:
        friend: Player = Walk2Gether.objects.get(player2=player).player1
        friendName = friend.user.username
        return HttpResponse(f'0:' + f'{friendName}')
    else:
        return HttpResponse(f'1:')

def acceptInviteWalk(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    try:
        match : Walk2Gether = Walk2Gether.objects.get(player2=player)
        match.accepted = True
        match.save()
        friendShip = Friendship.objects.get(player1=match.player1)
        multiplier = friendShip.step_multiplier
        return HttpResponse(f'0:' + f'{multiplier}')
    except ObjectDoesNotExist:
        return HttpResponse(f'1:')


def declineInviteWalk(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    try:
        match: Walk2Gether = Walk2Gether.objects.get(player2=player)
        match.delete()
        return HttpResponse(f'0:')
    except ObjectDoesNotExist:
        return HttpResponse(f'1:')


def cancelWalk(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    try:
        match: Walk2Gether = Walk2Gether.objects.get(player1=player)
        match.delete()
        return HttpResponse(f'0')
    except ObjectDoesNotExist:
        return HttpResponse(f'0:')

def checkAnswerWalk(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player

    try:
        match: Walk2Gether = Walk2Gether.objects.get(player1=player)
        friendShip = Friendship.objects.get(player1=match.player2)
        multiplier = friendShip.step_multiplier
        if match.accepted:
            return HttpResponse(f'0:' + f'{multiplier}')
        else:
            return HttpResponse(f'1:')
    except ObjectDoesNotExist:
        return HttpResponse(f'2:')

def goBack(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    player.coordinates = "0"
    player.save()
    return HttpResponse(f'0:')

def leaveWalk(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player

    try:
        match: Walk2Gether = Walk2Gether.objects.get(player1=player)
        match.isAlone = True
        match.save()
        return HttpResponse(f'0:')

    except ObjectDoesNotExist:
        try:
            match: Walk2Gether = Walk2Gether.objects.get(player2=player)
            match.isAlone = True
            match.save()
            return HttpResponse(f'0:')
        except ObjectDoesNotExist:
            return HttpResponse(f'2:')


def checkIfAlone(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    try:
        match: Walk2Gether = Walk2Gether.objects.get(player1=player)
        if match.isAlone:
            match.delete()
            return HttpResponse(f'0:')
        else:
            return HttpResponse(f'1:')
    except ObjectDoesNotExist:
        match: Walk2Gether = Walk2Gether.objects.get(player2=player)
        if match.isAlone:
            match.delete()
            return HttpResponse(f'0:')
        else:
            return HttpResponse(f'1:')


