from django.http import HttpResponse, JsonResponse

from .kerstin_utils import *


# -----------------------------------------------{ current level weather }----------------------------------------------

def set_level_current(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    match.current_weather = match.host.weathertokens.current_weather
    match.save()

    return HttpResponse(success_message)


def get_level_current(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    current: str = match.current_weather

    return HttpResponse(current)


# ---------------------------------------------------{ Level Tokens }---------------------------------------------------

def get_level_tokens(request) -> JsonResponse:
    match: Match = get_match(request)

    if not match:
        # safe=False so that Json doesn't have to return a dict
        return JsonResponse(failed_message, safe=False)

    t1 = match.host_token
    t2 = match.joined_token

    data: dict = {"t1": t1, "t2": t2}

    return JsonResponse(data)


def set_level_tokens(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    match.host_token = request.POST['t1']
    match.joined_token = request.POST['t2']

    return HttpResponse(success_message)


def get_host_token(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    resp: str = str(match.host_token) + "#" + str(match.host_token_id)
    return HttpResponse(resp)


def get_joined_token(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    resp: str = str(match.joined_token) + "#" + str(match.joined_token_id)
    return HttpResponse(resp)


def set_host_token(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    match.host_token_id = request.POST['id']
    state: str = request.POST['weather']
    match.host_token = string_2_weatherstate(state)

    match.save()

    return HttpResponse(success_message)


def set_joined_token(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    match.joined_token_id = request.POST['id']
    state: str = request.POST['weather']
    match.joined_token = string_2_weatherstate(state)

    match.save()

    return HttpResponse(success_message)


# --------------------------------------------------{ use level tokens }------------------------------------------------

def use_level_token(request) -> HttpResponse:
    match: Match = get_match(request)
    token_id: int = request.POST['id']

    if not match:
        return HttpResponse(failed_message)

    if request.POST['is_host_token']:
        match_success = use_host_token(match)

        host_token_table = get_token_table(match.host)
        host_success = use_token(host_token_table, token_id)

        if match_success and host_success:
            return HttpResponse(success_message)
        return HttpResponse(failed_message)

    # else is joined player
    match_success = use_joined_token(match)

    joined_token_table = get_token_table(match.joined_player)
    joined_success = use_token(joined_token_table, token_id)

    if match_success and joined_success:
        return HttpResponse(success_message)
    return HttpResponse(failed_message)


# ----------------------------------------------{ remove token from match }---------------------------------------------

def use_host_token(match: Match) -> int:
    host_token_state = string_2_weatherstate(match.host_token)
    set_level_current_to_token(match, host_token_state)

    match.host_token = WeatherState.none
    match.save()

    return 0


def use_joined_token(match: Match) -> int:
    joined_token_state = string_2_weatherstate(match.host_token)
    set_level_current_to_token(match, joined_token_state)

    match.joined_token = WeatherState.none
    match.save()

    return 0


def set_level_current_to_token(match: Match, state: WeatherState) -> int:
    match.current_weather = state
    match.save()
    return 0


# ----------------------------------------------{ remove token from player }--------------------------------------------

def use_token(wt: WeatherTokens, token_id: int) -> int:
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

    return 0
