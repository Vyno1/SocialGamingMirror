from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from typing import List

from .models import Player, Friendship

# ----------------------------------------------{Friendship Stuff}--------------------------------------------------- #

GET_DROP = "get_skin_drop_chance"
GET_SKINS = "get_skins_unlocked"
INC_DROP = "increase_skin_drop_chance"
RESET_DROP = "reset_skin_drop_chance"
INC_LVL = "increase_friendship_level"
UNLOCK = "unlock_skin"
GET = "GET"
POST = "POST"
WEATHER_SWAP_LEVEL = 10


#                                ---------------- view functions ----------------                                     #

# @Maxi (hab nix geändert)
def get_names(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    response = '0:'
    # Iterate through all players
    for player in Player.objects.all():
        response += f' {player.user.username}'
    return HttpResponse(response)


# @Maxi (hab nix geändert)
def get_friends(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    response = '0: '
    # Iterate through all the friendships of that player. Note that only the
    # players friends are displayed, not the followers (players that
    # friended the player without the player friending them back).
    for friendship in request.user.player.friends.all():
        response += f'{friendship.friend.user.username}' \
                    f' {friendship.level}' \
                    f' {friendship.skins_unlocked},'
    # This just removes the trailing comma left by the above iteration
    response = response[:-1]
    return HttpResponse(response)


# @Maxi
def get_followers(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    response = '0: '
    player = request.user.player
    for friendship in Friendship.objects.all():
        if player == friendship.friend:
            response += f'{friendship.friend.user.username},'
            response = response[:-1]
    return HttpResponse(response) if response != '0: ' else HttpResponse('1: No Followers')


# @Maxi
def add_friend(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player_name = request.user.username
    player = request.user.player
    friend_name = request.POST['name']
    friend = Player.objects.get(user__username=friend_name)

    response = f'0: friendship {player_name} -> {friend_name}'

    try:
        friendship = Friendship.objects.get(player=friend, friend=player)
        friendship.mutual = True
        response += ", their friendship is now mutual"
    except ObjectDoesNotExist:
        response += f", no friendship {friend_name} -> {player_name}"
        Friendship(player=player, friend=friend).save()
    except Exception as e:
        print(e)
        response += f", something went wrong, nothing changed."

    return HttpResponse(response)


# @Maxi
def disable_friend_info(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    player = request.user.player
    player.show_friend_info_screen = False
    player.save()
    return HttpResponse(f'0: friend-info screen disabled.')


# @Maxi
def get_friend_info_bool(request):
    return get_helper(request, request.user.player.show_friend_info_screen)


# @Maxi
def update_friendship_level(request):
    return friendship_helper(request, INC_LVL)


# @Maxi
def get_skin_drop_chance(request):
    return friendship_helper(request, GET_DROP)


# @Maxi
def increase_skin_drop_chance(request):
    return friendship_helper(request, INC_DROP)


# @Maxi
def reset_skin_drop_chance(request):
    return friendship_helper(request, RESET_DROP)


# @Maxi
def unlock_skin(request):
    return friendship_helper(request, UNLOCK)


#                               ---------------- helper functions ----------------                                    #

# @Maxi
def get_helper(request, response):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    else:
        return HttpResponse(f'0: {response}')


# @Maxi
def friendship_helper(request, response):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    try:
        friend = Player.objects.get(user__username=request.POST['friend_name'])
        friendship = Friendship.objects.get(player=request.user.player, friend=friend)
        if response == GET_DROP:
            response = f"0: {friendship.skin_drop_chance}"
        elif response == INC_DROP:
            friendship.skin_drop_chance += 0.05
            response = f"0: Skin drop chance increased:{friendship.skin_drop_chance}"
        elif response == RESET_DROP:
            friendship.skin_drop_chance = 0.05
            response = f"0: Skin drop chance reset:{friendship.skin_drop_chance}"
        elif response == INC_LVL:
            if friendship.level < 21:
                friendship.level += 1
                friendship.save()
            response = f"0: New friendship level:{friendship.level}"
        elif response == UNLOCK:
            index = request.POST["index"]
            friendship.skins_unlocked[index] = 1
            response = f"0: Unlocked Skin at index:{index}"
        return HttpResponse(response)
    except Exception as e:
        print(e)
        return HttpResponse(f"Either, theres no Friendship between {request.POST['friend_name']}"
                            f" and {request.user.username}, or something else went really wrong lol")


# ------------------------------------------------{End of File :)}--------------------------------------------------- #

# @Maxi
def get_best_friend(player: Player) -> Player:
    all_friendships: List[Friendship] = []
    all_friends: List[Player] = []
    for friendship in player.friends.all():
        if friendship.level >= WEATHER_SWAP_LEVEL:
            all_friendships.append(friendship)
    for friendship in player.followers.all():
        if friendship.level >= WEATHER_SWAP_LEVEL and friendship.mutual:
            all_friendships.append(friendship)
    all_friendships.sort(key=lambda fr_sh: fr_sh.level, reverse=True)
    for fs in all_friendships:
        friend = fs.player1 if player != fs.player1 else fs.player2
        all_friends.append(friend)

    if not all_friends:
        return None
    return all_friends[0]


# @Maxi
def get_friendship(player: Player, friend: Player) -> Friendship:
    try:
        friendship = player.friends.get(player2=friend)
    except ObjectDoesNotExist:
        try:
            friendship = player.followers.get(player1=friend)
        except ObjectDoesNotExist as error:
            print(f"No mutual friendship between \"{player.user.username}\" and \"{friend.user.username}\"!")
            print(error)
            friendship = None
    return friendship
