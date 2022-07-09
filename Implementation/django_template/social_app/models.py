from django.db import models
from django.contrib.auth.models import User
from .weather import WeatherState


# TODO: @team add your attributes and databases here

# A user consists mainly of a username and a password.
# A player is just a user with a points score.
class Player(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    score = models.IntegerField(default=0)
    show_friend_info_screen: bool = models.BooleanField(default=True)
    # @Kerstin added steps
    steps = models.IntegerField(default=0)
    # @Vyno added current scene
    scene: str = models.CharField(max_length=20, default="")

    def __str__(self):
        return self.user.username


# This represents a 2-player match of GravityJump
class Match(models.Model):
    # The host is mostly used as an identifier so that players can find the
    # match they have hosted or joined.
    host = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='host',
    )

    joined_player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='joined',
    )

    has_started = models.BooleanField(default=False)
    is_over = models.BooleanField(default=False)
    # @Kerstin removed ball attributes
    # TODO: Game State variables
    # @Kerstin pause menu fields
    is_paused = models.BooleanField(default=False)
    do_reset = models.BooleanField(default=False)
    do_exit = models.BooleanField(default=False)
    # @Vyno current Scene for swap
    current_scene: str = models.CharField(max_length=20, default="")


class Friendship(models.Model):
    # Because both these foreign keys are players, they need to be
    # distinguished using related_name. This way, the list of a player's
    # friends is unique and different from the list of a player's followers.
    # Followers are players who have befriended you, while friends are players
    # who you have befriended.
    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='friends',
    )
    friend = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='followers',
    )
    level = models.IntegerField(default=0)
    mutual = models.BooleanField(default=False)

    # Der Char an der Stelle i represented, ob Skin i schon freigeschaltet wurde als bool
    skins_unlocked = models.CharField(default="0000000000", max_length=10)
    skin_drop_chance = models.FloatField(default=0.05)

    # prohibit multiple instances of the same friendship
    class Meta:
        unique_together = ('player', 'friend')

    # These str methods are mostly used for debugging purposes. The
    # admin page of the site also uses this str method to display that
    # particular model.
    def __str__(self):
        return f'{self.player.user.username} -> {self.friend.user.username}'


class WeatherTokens(models.Model):
    owner = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,
    )

    # all weather tokens
    token0 = models.CharField(choices=WeatherState.choices, default=WeatherState.none, max_length=10)
    token1 = models.CharField(choices=WeatherState.choices, default=WeatherState.none, max_length=10)
    token2 = models.CharField(choices=WeatherState.choices, default=WeatherState.none, max_length=10)
    token3 = models.CharField(choices=WeatherState.choices, default=WeatherState.none, max_length=10)
    token4 = models.CharField(choices=WeatherState.choices, default=WeatherState.none, max_length=10)
    friend_token = models.CharField(choices=WeatherState.choices, default=WeatherState.none, max_length=10)
    current_weather = models.CharField(choices=WeatherState.choices, default=WeatherState.none, max_length=10)
    # TODO: check if already got daily token via bool / date
    received_daily_token = models.BooleanField(default=False)

    def __str__(self):
        return self.owner.user.username
