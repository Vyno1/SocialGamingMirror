from django.http import HttpResponse, JsonResponse

from .kerstin_utils import *


def set_level_current(request) -> HttpResponse:
    match: Match = get_match(request)

    if not match:
        return HttpResponse(failed_message)

    match.current_weather = match.host.weathertokens.current_weather
    match.save()

    return HttpResponse(success_message)
