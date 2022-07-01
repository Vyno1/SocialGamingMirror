# views.py file for game logic

from django.http import HttpResponse
from .models import Match
from .pause import get_match, success_message


def update(request):
    """sets current values of game state when sth changes"""
    # TODO: set all variables in database STEPS?
    match: Match = get_match(request)

    # ...
    return HttpResponse(success_message)

