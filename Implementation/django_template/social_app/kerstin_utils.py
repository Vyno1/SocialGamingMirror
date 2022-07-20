from social_app.models import Player, Match, WeatherTokens
from social_app.weatherstate import WeatherState

# ----------------------------------------------------{ query errors }--------------------------------------------------

not_signed_in_message = '1: user not signed in'
wrong_method_message = '1: incorrect request method'
not_a_player_message = '1: user is not a player'
no_match_message = '1: user has no match'

# ---------------------------------------------------{ status messages }------------------------------------------------

success_message = '0: success'
failed_message = '1: error'

# ----------------------------------------------------{ return bools }--------------------------------------------------

bool_true = 'true'
bool_false = 'false'


# -------------------------------------------------{ get match helper }-------------------------------------------------

def get_match(request):
    if not hasattr(request.user, 'player'):
        return None

    player: Player = request.user.player

    player_is_host: bool = player.host.all().count() == 1
    match: Match = Match.objects.get(host=player) if player_is_host else Match.objects.get(joined_player=player)

    if not match:
        return None

    return match


# ----------------------------------------------{ get token table helper }----------------------------------------------

def get_token_table(player: Player):
    wt: WeatherTokens = WeatherTokens.objects.get(owner=player)

    if not wt:
        return None

    return wt


# ----------------------------------------------{ string to weather state }---------------------------------------------

def string_2_weatherstate(string: str) -> WeatherState:
    if string == "sun":
        return WeatherState.sun
    if string == "rain":
        return WeatherState.sun
    if string == "snow":
        return WeatherState.snow
    if string == "wind":
        return WeatherState.wind
    if string == "thunder":
        return WeatherState.thunder

    return WeatherState.none

# --------------------------------------------------------{ END }-------------------------------------------------------
