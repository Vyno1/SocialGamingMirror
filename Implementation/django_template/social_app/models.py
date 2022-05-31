from django.db import models
from django.contrib.auth.models import User


# A user consists mainly of a username and a password.
# A player is just a user with a points score.
class Player(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username


# This represents a 2-player match of TiltBall
class Match(models.Model):
    # The host is mostly used as an identifier so that players can find the
    # match they have hosted or joined.
    host = models.OneToOneField(
        Player,
        on_delete=models.CASCADE,
    )
    # The TiltBall match goes through these phases: First all these values
    # are false. Then the game starts, so has_started is true. Then the
    # guest passes the ball to the host, so host_has_ball is True.
    # host_has_ball switches from True to False over and over as the players
    # pass the ball between each other, until the ball hits an obstacle and
    # the game ends, at which point is_over is True.
    host_has_ball = models.BooleanField(default=False)
    has_started = models.BooleanField(default=False)
    is_over = models.BooleanField(default=False)
    # The x value of the ball's position as it passes between players
    position = models.DecimalField(default=0, max_digits=30, decimal_places=20)
    # The velocity of the ball is passed along so that passing is more dynamic
    velocity_x = models.DecimalField(
        default=0, max_digits=30, decimal_places=20)
    velocity_y = models.DecimalField(
        default=0, max_digits=30, decimal_places=20)


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

    # The addition of this class ensures that 2 players cannot befriend each
    # other more than once, but it is still possible for a player to
    # befriend any number of different players and for that player to be
    # befriended by any number of different players. If you prefer
    # friendships always being symmetric, i.e. if player A is the friend
    # of player B, player B is automatically the friend of player A,
    # this can also be done.
    class Meta:
        unique_together = ('player', 'friend')

    # These str methods are mostly used for debugging purposes. The
    # admin page of the site also uses this str method to display that
    # particular model.
    def __str__(self):
        return f'{self.player.user.username} -> {self.friend.user.username}'
