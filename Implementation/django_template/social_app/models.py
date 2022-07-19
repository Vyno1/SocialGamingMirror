import datetime

from django.db import models
from django.contrib.auth.models import User

from .weatherstate import WeatherState


# TODO: @team add your attributes and databases here

# A user consists mainly of a username and a password.
# A player is just a user with a points score.
class Player(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    # @Maxi added unlocked levels
    levels_unlocked = models.IntegerField(default=0)
    # @Maxi added info-screen bool
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
        default=None,
    )
    # @Robin waitinglist for hosts
    guest_ready = models.BooleanField(default=False)
    host_left = models.BooleanField(default=False)
    guest_left = models.BooleanField(default=False)

    # @Robin attributes for skins
    host_skin = models.CharField(max_length=2, default="0")
    guest_skin = models.CharField(max_length=2, default="0")

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
    # @Vyno bool for scene swap
    sceneChanges: bool = models.BooleanField(default=False)
    # @Maxi bool for betweenlevels
    friendship_is_updated: bool = models.BooleanField(default=False)

    class Meta:
        unique_together = ('host', 'joined_player')

    def __str__(self):
        relation = "<-->"
        return f'{self.host.user.username} {relation} {self.joined_player.user.username}'


class WaitingList(models.Model):
    waitinghost = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='waitinghost',
    )

    def __str__(self):
        return self.waitinghost.user.username


class InviteMatch(models.Model):
    # The host is mostly used as an identifier so that players can find the
    # match they have hosted or joined.
    Inviter = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='inviter',
    )

    invited_player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='invited',
    )

    accepted = models.BooleanField(default=False)
    started = models.BooleanField(default=False)

    class Meta:
        unique_together = ('Inviter', 'invited_player')

    def __str__(self):
        relation = "<-->"
        return f'{self.Inviter.user.username} {relation} {self.invited_player.user.username}'


class Friendship(models.Model):
    # Because both these foreign keys are players, they need to be
    # distinguished using related_name. This way, the list of a player's
    # friends is unique and different from the list of a player's followers.
    # Followers are players who have befriended you, while friends are players
    # who you have befriended.
    player1 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='friends',
    )
    player2 = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='followers',
    )
    level = models.IntegerField(default=0)
    mutual = models.BooleanField(default=False)

    # Der Char an der Stelle i represented, ob Skin i schon freigeschaltet wurde als bool
    skins_unlocked = models.CharField(default="0000000000", max_length=10)
    skin_drop_chance = models.FloatField(default=0.05)
    step_multiplier = models.FloatField(default=1.0)

    # prohibit multiple instances of the same friendship
    class Meta:
        unique_together = ('player1', 'player2')

    # These str methods are mostly used for debugging purposes. The
    # admin page of the site also uses this str method to display that
    # particular model.
    def __str__(self):
        relation = "-->" if not self.mutual else "<-->"
        return f'{self.player1.user.username} {relation} {self.player2.user.username}'


class WeatherTokens(models.Model):
    owner = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,
        primary_key=True
    )

    # all weather tokens
    token0 = models.CharField(choices=WeatherState.choices, default=WeatherState.none, max_length=10)
    token1 = models.CharField(choices=WeatherState.choices, default=WeatherState.none, max_length=10)
    token2 = models.CharField(choices=WeatherState.choices, default=WeatherState.none, max_length=10)
    token3 = models.CharField(choices=WeatherState.choices, default=WeatherState.none, max_length=10)
    token4 = models.CharField(choices=WeatherState.choices, default=WeatherState.none, max_length=10)

    current_weather = models.CharField(choices=WeatherState.choices, default=WeatherState.none, max_length=10)

    # date format: datetime.date(year, month, day)
    date_of_last_daily_claim = models.DateField(default=datetime.date(1969, 1, 1))
    used_shared = models.BooleanField(default=False)

    def __str__(self):
        return "tokens of " + str(self.owner.user.username)
