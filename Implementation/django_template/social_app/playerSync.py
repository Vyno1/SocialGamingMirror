from django.http import HttpResponse
from .models import Player, Match

def sync_players_receive(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    response = '0: '

    # Get Player by username
    myPlayer: Player = Player.objects.get(user__username=request.user.username)
    # Update position and gravity information
    myPlayer.position = request.POST["player_position"]
    myPlayer.gravity_normal = request.POST["gravity_normal"]
    myPlayer.save()

    return HttpResponse(response)

def sync_players_send(request):
    if not request.user.is_authenticated:
        return HttpResponse('user not signed in')
    if request.method != 'POST':
        return HttpResponse('incorrect request method')
    response = '0: '

    # Get myPlayer by username, get joined player through match via myPlayer
    myPlayer: Player = Player.objects.get(user__username=request.user.username)
    match: Match = Match.objects.get(host=myPlayer)
    joinedPlayer: Player = match.joined_player
    # Append position and gravity information to response
    response += joinedPlayer.position
    response += joinedPlayer.gravity_normal

    # Removes the trailing comma left by the above iteration and send response
    response = response[:-1]
    return HttpResponse(response)