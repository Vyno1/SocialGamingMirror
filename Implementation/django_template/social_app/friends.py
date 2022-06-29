from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from .models import Player, Friendship


# ----------------------------------------------{Friendship Stuff}----------------------------------------------------#

# view functions:
# get_names, get_friends, get_followers, add_friend, update_friendship_level, disable_friend_info, get_friend_info_bool,
#
# helper functions:
# test_get_issues


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
                    f' {friendship.level},'
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
            response += f'{friendship.friend.user.username}' \
                        f' {friendship.friend.level},'
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
def update_friendship_level(request):
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    try:
        friend = Player.objects.get(user__username=request.POST['friend_name'])
        friendship = Friendship.objects.get(player=request.user.player, friend=friend)
        if friendship.level < 101:
            friendship.level += 1
            friendship.skin1_unlocked = True if friendship.level == 5 else False
            friendship.skin2_unlocked = True if friendship.level == 10 else False
            friendship.save()
        return HttpResponse("0: Updated friendship level successfully")
    except Exception as e:
        print(e)
        return HttpResponse("Something went wrong while updating friendship level")


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
    no_issues = test_get_issues(request)
    return no_issues \
        if isinstance(no_issues, HttpResponse) \
        else HttpResponse(f'0: {request.user.player.show_friend_info_screen}')


# @Maxi
def get_skin_unlocked(request):
    no_issues = test_get_issues(request)
    if isinstance(no_issues, HttpResponse):
        return no_issues
    else:
        try:
            friend = Player.objects.get(user__username=request.POST['friend_name'])
            friendship = Friendship.objects.get(player=request.user.player, friend=friend)
            response = f"0: {friendship.skins_unlocked[int(request.POST['skin_index'])]}"
            return HttpResponse(response)
        except ValueError as val:
            print(val)
            return HttpResponse(f"skin_index must be an integer!")
        except IndexError as index:
            print(index)
            return HttpResponse(f"skin_index out of range!")
        except Exception as e:
            print(e)
            return HttpResponse(f"No Friendship between {request.POST['friend_name']} and {request.user.username}")


# @Maxi
def test_get_issues(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'GET':
        return HttpResponse(f'incorrect request method.')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')
    else:
        return 1
