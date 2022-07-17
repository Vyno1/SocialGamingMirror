from typing import List

from django.http import HttpResponse
from .models import Player, Friendship, Match
from django.core.exceptions import ObjectDoesNotExist


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
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    player = request.player
    player.levels_unlocked += 1 if player.levels_unlocked < int(request.POST["max_level"]) else 0
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

    player: Player = request.user.player
    # Response scheme = "0: [is_host: bool]
    #                       [other_player_name: string]
    #                       [levels_unlocked: int (-1 if you're not the host)]
    #                       [friendship_level: int (-1 if no friendship exists)]

    response: str = "0: "
    response += "1 " if player.host.all().count() >= 1 else "0 "

    other_name: str = f"{player.host.get().joined_player}" if response.startswith("0: 1") \
        else f"{player.joined.get().host}"
    response += f"{other_name} "

    response += f"{player.levels_unlocked} " if response.startswith("0: 1") else "-1 "

    friendship_level: int = -1
    for friendship in player.friends.all():
        if friendship.player2.user.username == other_name:
            if friendship.mutual:
                friendship_level = friendship.level
    for friendship in player.followers.all():
        if friendship.player1.user.username == other_name:
            if friendship.mutual:
                friendship_level = friendship.level
    response += f"{friendship_level} "

    return HttpResponse(response)


# @Maxi
def is_friendship_updated(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    response = "0" if request.user.player.joined.friendship_is_updated else "1"
    return HttpResponse(response)


# @Maxi
def update_friendship(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    match: Match = request.user.player.host
    match.friendship_is_updated = True
    match.save()

    return HttpResponse("0: Friendship updated.")
