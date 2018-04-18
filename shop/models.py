from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.


class Player(models.Model):
    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Developer(models.Model):
    def __str__(self):
        return self.user.username

    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Game(models.Model):
    def __str__(self):
        return self.title

    title = models.CharField(max_length=30, null=False, blank=False, unique=False)
    price = models.FloatField(null=False, blank=False, unique=False)
    url = models.URLField(max_length=300, null=False, blank=False, unique=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE)


class State(models.Model):
    state = models.CharField(null=True, blank=True, max_length=100, default="")
    score = models.FloatField(null=True, blank=True, default=0)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)


# In order to find out if the user has bought a game
# it is enough to call Transaction.objects.filter(game=g_id, player=p_id)
# Based on the result set we derive if the user purchased the game or not.
class Transaction(models.Model):
    def __str__(self):
        return "Transaction:" + \
               self.game.title + \
               "(" + str(self.game.id) + ")" + "-" \
               + self.player.user.username + "(" + str(self.player.id) + ")" + \
               "-" + str(self.timestamp)

    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    paid_amount = models.FloatField()
    timestamp = models.DateField(default=timezone.now)
