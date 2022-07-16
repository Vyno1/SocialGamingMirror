from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .models import Player, Match, WaitingList, InviteMatch

def inviteFriend(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player = request.user.player
    friend_name = request.POST['name']
    friend = Player.objects.get(user__username=friend_name)

    count1 = friend.host.all().count()
    count2 = friend.joined.all().count()
    count3 = friend.waitinghost.all().count()
    count4 = friend.invited.all().count()
    count = count1 + count2 + count3 + count4
    if count > 0 and not friend.user.is_authenticated:
        # friend already in a lobby
        return HttpResponse(f'1:')
    else:
        InviteMatch(Inviter=player, invited_player=friend).save()
        return HttpResponse(f'0:')

def checkIfInvited(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player : Player = request.user.player
    count = player.invited.all().count()
    if count > 0:
        friend: Player = InviteMatch.objects.get(invited_player=player).Inviter
        friendName = friend.user.username
        return HttpResponse(f'0:' + f'{friendName}')
    else:
        return HttpResponse(f'1:')

def acceptInvite(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    try:
        match : InviteMatch = InviteMatch.objects.get(invited_player=player)
        match.accepted = True
        match.save()
        return HttpResponse(f'0:')
    except ObjectDoesNotExist:
        return HttpResponse(f'1:')


def declineInvite(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    try:
        match: InviteMatch = InviteMatch.objects.get(invited_player=player)
        match.delete()
        return HttpResponse(f'0:')
    except ObjectDoesNotExist:
        return HttpResponse(f'1:')

def start(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    match : InviteMatch = InviteMatch.objects.get(Inviter=player)
    friend: Player = match.invited_player
    match.started = True
    match.save()
    Match(host=player, joined_player=friend).save()
    return HttpResponse(f'0:')

def cancel(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    try:
        match: InviteMatch = InviteMatch.objects.get(Inviter=player)
        match.delete()
        return HttpResponse(f'0')
    except ObjectDoesNotExist:
        return HttpResponse(f'0:')

def checkAnswer(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player

    try:
        match: InviteMatch = InviteMatch.objects.get(Inviter=player)
        if match.accepted:
            return HttpResponse(f'0:')
        else:
            return HttpResponse(f'1:')
    except ObjectDoesNotExist:
        try:
            match: InviteMatch = InviteMatch.objects.get(invited_player=player)
            if match.started:
                match.delete()
                return HttpResponse(f'3:')
            else:
                return HttpResponse(f'1:')
        except ObjectDoesNotExist:
            return HttpResponse(f'2:')

