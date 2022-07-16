import random
from typing import List

from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .models import Player, Friendship, Match

# ----------------------------------------------{Friendship Stuff}--------------------------------------------------- #
WEATHER_SWAP_LEVEL = 10
#                                ---------------- view functions ----------------                                     #


# @Maxi
def get_names(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    response = '0:'
    # Iterate through all players
    for player in Player.objects.all():
        response += f' {player.user.username}'
    return HttpResponse(response)


# @Maxi
def get_friends(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    response = '0: '
    for friendship in request.user.player.friends.all():
        response += f'{friendship.player2.user.username} ' \
                    f'{friendship.level} ' \
                    f'{friendship.skins_unlocked} ' \
                    f'{friendship.skin_drop_chance} ' \
                    f'{friendship.step_multiplier},'
    for friendship in request.user.player.followers.all():
        response_text = f'{friendship.player1.user.username} ' \
                        f'{friendship.level} ' \
                        f'{friendship.skins_unlocked} ' \
                        f'{friendship.skin_drop_chance} ' \
                        f'{friendship.step_multiplier},'
        response += response_text if friendship.mutual else ""
    response = response[:-1]
    return HttpResponse(response) if response != '0: ' else HttpResponse('1: No Friends...')


# @Maxi
def get_followers(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    response = '0: '
    for friendship in request.user.player.followers.all():
        response += f'{friendship.player1.user.username},' if not friendship.mutual else ""
    response = response[:-1]
    return HttpResponse(response) if response != '0:' else HttpResponse('1: No Followers...')


# @Maxi
def add_friend(request) -> HttpResponse:
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
        # Wenn es schon eine Freundschaft von friend zu mir gibt, setze sie auf mutual, somit bin ich fake-follower
        friendship = Friendship.objects.get(player1=friend, player2=player)
        friendship.mutual = True
        friendship.save()
        response += ", their friendship is now mutual"
    except ObjectDoesNotExist:
        response += f", no friendship {friend_name} -> {player_name}"
        Friendship(player1=player, player2=friend).save()
    except Exception as e:
        print(e)
        response = f"Something went wrong, nothing changed."
    return HttpResponse(response)


# @Maxi
def disable_friend_info(request) -> HttpResponse:
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
def get_friend_info_bool(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    else:
        return HttpResponse(f'0: {request.user.player.show_friend_info_screen}')


# @Maxi
def update_friendship_level(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    try:
        friend = Player.objects.get(user__username=request.POST['friend_name'])
        friendship = get_friendship(request.user.player, friend)
        if friendship.mutual:
            if friendship.level < 10000:
                friendship.level += 1
            if friendship.step_multiplier <= 2:
                friendship.step_multiplier += 0.05
            if friendship.skins_unlocked != "1" * len(friendship.skins_unlocked):
                if friendship.skin_drop_chance <= 0.70:
                    friendship.skin_drop_chance += 0.05
                if random.random() < friendship.skin_drop_chance:
                    index = 0
                    unlocked = friendship.skins_unlocked
                    while unlocked[index] == "1":
                        # random.random() returned nur [0, 1), deswegen ist die length fine und nicht out of bounds
                        index = int(random.random() * len(unlocked))
                    unlocked_list = list(unlocked)
                    unlocked_list[index] = "1"
                    friendship.skins_unlocked = "".join(unlocked_list)
                    friendship.skin_drop_chance = 0.05
            friendship.save()
            response = f'0: {friendship.level} ' \
                       f'{friendship.skins_unlocked} ' \
                       f'{friendship.skin_drop_chance} ' \
                       f'{friendship.step_multiplier}'
            return HttpResponse(response)
    except ObjectDoesNotExist:
        return HttpResponse(f"Either, theres no Friendship between \"{request.POST['friend_name']}\""
                            f" and \"{request.user.username}\", or \"{request.POST['friend_name']}\" doesn't exist.")
    except Exception as e:
        print(e)
        return HttpResponse(f"ObjectDoesNotExist-Exception-Handling doesnt work, "
                            f"or something else went really wrong lol")

#                               ---------------- helper functions ----------------                                    #


# @Maxi
def get_best_friend(player: Player) -> Player | None:
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

    if len(all_friends) == 0:
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


# @Robin
def get_mutualfriends(request) -> HttpResponse:
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    response = '0: '
    for friendship in request.user.player.friends.all():
        friend: Player = friendship.player2
        if friendship.mutual and friend.user.is_authenticated:
            response += f'{friendship.player2.user.username},'
    for friendship in request.user.player.followers.all():
        friend: Player = friendship.player1
        if friendship.mutual and friend.user.is_authenticated:
            response += f'{friendship.player1.user.username},'
    response = response[:-1]
    return HttpResponse(response) if response != '0: ' else HttpResponse('1: No Friends...')

# ------------------------------------------------{End of File :)}--------------------------------------------------- #
