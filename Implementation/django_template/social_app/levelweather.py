from django.http import HttpResponse, JsonResponse

from .kerstin_utils import *


def set_level_current(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    match.current_weather = match.host.weathertokens.current_weather
    match.save()

    return HttpResponse(success_message)


# sets current to token
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
    match.host_token = WeatherState.none
    match.save()

    return 0


def use_joined_token(match: Match) -> int:
    match.joined_token = WeatherState.none
    match.save()

    return 0


# ----------------------------------------------{ remove token from match }---------------------------------------------

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
