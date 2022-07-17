from django.http import HttpResponse
from .models import Player, Match

def sync_players_receive(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    response = '0: '

    # Get Player by username
    myPlayer: Player = request.user.player
    # Update position and gravity information
    myPlayer.position = request.POST['player_position']
    myPlayer.save()
    response += myPlayer.position
    return HttpResponse(response)

def sync_players_send(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    response = '0: '

    # Get Player by user and deciver if host
    player: Player = request.user.player
    isHost = player.host.all().count() == 1
    # Append position and gravity information to response
    if isHost:
        match: Match = Match.objects.get(host=player)
        response += match.joined_player.position
    else:
        match: Match = Match.objects.get(joined_player=player)
        response += match.host.position
    return HttpResponse(response)


def gravity_receive(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    response = '0: Gravity received'

    # Get Match by user !!only the host switches and thus sends gravity_state!!
    match: Match = Match.objects.get(host=request.user.player)
    # Update gravity information in match
    match.gravity_normal = request.POST['gravity_normal'] == '1'
    match.save()

    return HttpResponse(response)

def gravity_send(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    response = '0: '

    # Get Player by user
    player: Player = request.user.player
    isHost = player.host.all().count() == 1
    # Get Match by Player
    if isHost:
        match: Match = Match.objects.get(host=player)
    else:
        match: Match = Match.objects.get(joined_player=player)
    # Append gravity information to response
    response += str(match.gravity_normal)

    return HttpResponse(response)