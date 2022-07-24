from django.http import HttpResponse, JsonResponse

from .kerstin_utils import *


# -----------------------------------------------{ current level weather }----------------------------------------------

def set_level_current(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    match.current_weather = match.host.weathertokens.current_weather
    print("setting level current to " + match.current_weather)

    match.save()

    return HttpResponse(success_message)


def get_level_current(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    current: str = match.current_weather
    print("getting current: " + current)

    return HttpResponse(current)


# ---------------------------------------------------{ Level Tokens }---------------------------------------------------

def get_level_tokens(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    t_host = match.host_token
    t_joined = match.joined_token

    resp: str = str(t_host) + "#" + str(t_joined)
    print("Anfrage level tokens, returned " + resp)

    return HttpResponse(resp)


def set_level_tokens(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    match.host_token = request.POST['t_host']
    match.joined_token = request.POST['t_join']
    # match.host_token_id = request.POST['t_host_id']
    # match.joined_token_id = request.POST['t_join_id']

    if request.POST['t_host'] == "none":
        match.host_token_id = -1

    if request.POST['t_join'] == "none":
        match.joined_token_id = -1

    print("set level tokens, got hosttoken: " + request.POST['t_host'] + " and joined: " + request.POST['t_join'])

    return HttpResponse(success_message)


def get_host_token(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    resp: str = str(match.host_token) + "#" + str(match.host_token_id)
    print("Anfrage nach host token, returned " + resp)

    return HttpResponse(resp)


def get_joined_token(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    resp: str = str(match.joined_token) + "#" + str(match.joined_token_id)
    print("Anfrage nach joined token, returned " + resp)

    return HttpResponse(resp)


def set_host_token(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    match.host_token_id = request.POST['id']
    state: str = request.POST['weather']
    match.host_token = string_2_weatherstate(state)

    print("set host token to weather " + match.host_token + " with id " + str(match.host_token_id))

    match.save()

    return HttpResponse(success_message)


def set_joined_token(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    match.joined_token_id = request.POST['id']
    state: str = request.POST['weather']
    match.joined_token = string_2_weatherstate(state)

    print("set join token to weather " + match.joined_token + " with id " + str(match.joined_token_id))

    match.save()

    return HttpResponse(success_message)


# --------------------------------------------------{ use level tokens }------------------------------------------------

def use_level_token(request) -> HttpResponse:
    match: Match = get_match(request)
    token_id: int = request.POST['id']

    print("use token, isHostToken == " + request.POST['is_host_token'])

    if not match:
        return HttpResponse(failed_message + ": no match")

    if request.POST['is_host_token'] == "true":
        match_success = use_host_token(match)

        if match_success:
            return HttpResponse(success_message)
        return HttpResponse(failed_message + ": token removal failed")

    # else is joined player
    match_success = use_joined_token(match)

    if match_success:
        return HttpResponse(success_message)
    return HttpResponse(failed_message)


# ----------------------------------------------{ remove token from match }---------------------------------------------

def use_host_token(match: Match) -> bool:
    host_token_state = string_2_weatherstate(match.host_token)
    if host_token_state == "none":
        return False

    set_level_current_to_token(match, host_token_state)

    # reset tokens to default
    match.host_token = WeatherState.none
    match.host_token_id = -1
    match.save()

    return True


def use_joined_token(match: Match) -> bool:
    joined_token_state = string_2_weatherstate(match.joined_token)
    if joined_token_state == "none":
        return False

    set_level_current_to_token(match, joined_token_state)

    # reset tokens to default
    match.joined_token = WeatherState.none
    match.joined_token_id = -1
    match.save()

    return True


def set_level_current_to_token(match: Match, state: WeatherState) -> bool:
    match.current_weather = state
    match.save()
    return True


# ----------------------------------------------{ remove token from player }--------------------------------------------


def remove_player_tokens(request):
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message + ": no match")

    # get weather token tables of the players and remove the stored tokens
    host: Player = match.host
    joined: Player = match.joined_player
    host_table = get_token_table(host)
    joined_table = get_token_table(joined)

    host_id: int = int(request.POST['t_host'])
    joined_id: int = int(request.POST['t_join'])

    host_success: bool = use_token(host_table, host_id)
    joined_success: bool = use_token(joined_table, joined_id)

    if host_success and joined_success:
        return HttpResponse(success_message)
    return HttpResponse(failed_message + ": removing tokens went wrong")


def use_token(wt: WeatherTokens, token_id: int) -> bool:
    if token_id == 0:
        wt.token0 = WeatherState.none
    if token_id == 1:
        wt.token1 = WeatherState.none
    if token_id == 2:
        wt.token2 = WeatherState.none
    if token_id == 3:
        wt.token3 = WeatherState.none
    if token_id == 4:
        wt.token4 = WeatherState.none
    if token_id == 5:
        wt.used_shared = True

    # if id was -1 nothing happens because no tokens were used
    return True
