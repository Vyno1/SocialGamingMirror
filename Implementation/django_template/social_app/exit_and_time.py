from django.http import HttpResponse

from .models import Player, Match

# -------------------------------------------------{Exit Stuff}------------------------------------------------------ #


# @Maxi
def handle_quit(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    player_is_host: bool = player.host.all().count() == 1
    if not (player_is_host or player.joined.all().count() == 1):
        return HttpResponse(f"2: Player is not in a match!")

    match: Match = player.host.first() if player_is_host else player.joined.first()
    if not match.other_player_closed_game:
        return HttpResponse(f"1: Other Player didn't close the game.")
    match.delete()

    other: Player = match.joined_player if player_is_host else match.host
    other.scene = "MainMenu"
    other.save()
    player.scene = "DisconnectedMenu"
    player.save()

    return HttpResponse(f"0: Other player quit, current scene is now: {player.scene}")


# @Maxi
def set_quit(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    if player.host.all().count() != 1 and player.joined.all().count() != 1:
        return HttpResponse(f"1: No match that needs to be handled found.")

    match: Match = player.host.first() if player.host.all().count() == 1 else player.joined.first()
    match.other_player_closed_game = True
    match.save()

    return HttpResponse(f"0: Told server that the game was closed.")

# -------------------------------------------------{Time Stuff}------------------------------------------------------ #


# @Maxi
def get_localtime(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    return HttpResponse(f"0: {'true' if request.user.player.joined.first().host.is_day else 'false'}")


# @Maxi
def send_localtime(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player: Player = request.user.player
    player.is_day = bool(int(request.POST["is_day"]))
    player.save()

    return HttpResponse(f"0: Updated hosts is_day attribute")

# -----------------------------------------------------{EOF}--------------------------------------------------------- #
