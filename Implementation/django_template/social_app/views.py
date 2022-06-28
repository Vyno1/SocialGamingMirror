from django.http import HttpResponse

from .models import Player, Friendship, Match
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist

from django.contrib.auth import logout


# If this file becomes too large it is recommended to split it up into
# multiple files. This file is not special, just make sure that the correct
# file and view function is linked to the correct URL in urls.py.
# TODO: @team make own source files and reference the methods in urls.py


# ------------------------------------------------{Login Stuff}-------------------------------------------------------#
# USER AUTHENTICATION: check_auth, signout, signin, signup


def check_auth(request):
    if request.user.is_authenticated:
        return HttpResponse(f'0: "{request.user.username}" is authenticated')
    else:
        return HttpResponse('1: user is not authenticated')


def signout(request):
    logout(request)
    return HttpResponse('0: successful logout')


def signin(request):
    if request.user.is_authenticated:
        return HttpResponse(f'1: "{request.user.username}" already signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    username = request.POST['username']
    password = request.POST['password']

    # authenticate() only returns a user if username and password are correct
    user = authenticate(request, username=username, password=password)
    if user is None:
        return HttpResponse(f'could not authenticate.')
    login(request, user)
    return HttpResponse('0: successful signin')


def signup(request):
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    # Instead of checking for the form data ourselves, we use the already
    # existing UserCreationForm.
    form = UserCreationForm(request.POST)
    if not form.is_valid():
        return HttpResponse(f'invalid form: {form}')
    # This creates a user from that form
    form.save()
    # This logs in that user
    username = form.cleaned_data.get('username')
    raw_password = form.cleaned_data.get('password1')
    # We don't have to check if the username and password are correct
    # because we just created that exact user.
    user = authenticate(username=username, password=raw_password)
    login(request, user)
    # Create the user's player
    player = Player(user=user)
    # Don't forget to save at the end of all the changes to table contents
    player.save()
    return HttpResponse('0: successful signup')


# ----------------------------------------------{Friendship Stuff}----------------------------------------------------#

# FRIENDS LIST:
# view functions: get_names, get_friends, add_friend,
# helper functions: update_friendship_level, update_all_friendship_levels


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
            # This just removes the trailing comma left by the above iteration
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
    except Exception:
        response += f", something went wrong, nothing changed."

    return HttpResponse(response)


# @Maxi
def update_friendship_level(friendship):
    # Momentan kann man nur 100 level haben, dann Skin :)
    if friendship.level < 101:
        friendship.level += 1
        friendship.save()


# @Maxi
def disable_friend_info(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    player_name = request.POST['player']
    player = Player.objects.get(user__username=player_name)
    player.show_friend_info_screen = False
    player.save()
    return HttpResponse(f'0: friend-info screen disabled.')


def get_friend_info_bool(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    return HttpResponse(f'0: {request.user.player.show_friend_info_screen}')


# ---------------------------------------------{Leaderboard Stuff}----------------------------------------------------#


# LEADERBOARD: get_scores, edit_score
def get_scores(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    response = '0: '
    # Iterates over all players
    for player in Player.objects.all():
        # Remember you can't do player.username because the player does not
        # have a username, only the player's user.
        response += f'{player.user.username} {player.score},'
    # Removes the trailing comma left by the above iteration
    response = response[:-1]
    return HttpResponse(response)


def edit_score(request):
    if not request.user.is_authenticated:
        return HttpResponse('user not signed in')
    if request.method != 'POST':
        return HttpResponse('incorrect request method')
    # Get the score
    score = request.POST['score']
    # Change the player's score
    request.user.player.score = int(score)
    # Save that change
    request.user.player.save()
    response = f'0: changed the score of {request.user.username} to {score}'
    return HttpResponse(response)


# ------------------------------------------------{Match Stuff}-------------------------------------------------------#

# TILTBALL: host_match, join_match, get_match, end_match

def host_match(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if not hasattr(request.user, 'player'):
        return HttpResponse(f'user is not a player')

    player = request.user.player
    if hasattr(player, 'match'):
        # The player has at some point hosted a match, so this is reset to
        # its initial state.
        player.match.host_has_ball = False
        player.match.has_started = False
        player.match.is_over = False
        player.match.position = 0
        player.match.save()
        return HttpResponse(f'0: reset match')
    else:
        # The player has never hosted a match, so the default values of the
        # newly created match are already correct.
        match = Match(host=player)
        match.save()
        return HttpResponse(f'0: created match')


def join_match(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')

    host_name = request.POST['host']
    host = Player.objects.get(user__username=host_name)
    if hasattr(host, 'match'):
        host.match.host_has_ball = True
        host.match.has_started = True
        host.match.save()
        return HttpResponse(f'0: joined match, started match')
    else:
        return HttpResponse(f'no match with host {host_name} exists')


def get_match(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')

    host_name = request.POST['host']
    # Keyword attributes are very powerful. Look at the Django documentation
    # for more details. This line fetches the player that has a user that
    # has a username that equals name. The __ is equivalent to a dot.
    # user.username in regular code becomes the user__username parameter of
    # the get function. Remember: players don't have usernames, only the
    # players' users have usernames.
    host = Player.objects.get(user__username=host_name)

    if not hasattr(host, 'match'):
        return HttpResponse(f'no match with host {host_name} exists')
    if not host.match.has_started:
        return HttpResponse(f'match has not started')
    if host.match.is_over:
        return HttpResponse(f'2: match is over')
    match_ball = f'{host.match.position} '
    match_ball += f'{host.match.velocity_x} '
    match_ball += f'{host.match.velocity_y}'
    if host.match.host_has_ball:
        return HttpResponse(f'0: {match_ball}')
    else:
        return HttpResponse(f'1: {match_ball}')


def end_match(request):
    if not request.user.is_authenticated:
        return HttpResponse(f'user not signed in')
    if request.method != 'POST':
        return HttpResponse(f'incorrect request method.')
    host_name = request.POST['host']
    host = Player.objects.get(user__username=host_name)
    if not hasattr(host, 'match'):
        return HttpResponse(f'no match with host {host_name} exists')
    host.match.is_over = True
    host.match.save()
    return HttpResponse(f'0: ended match')

# ----------------------------------------------------{EOF}-----------------------------------------------------------#
