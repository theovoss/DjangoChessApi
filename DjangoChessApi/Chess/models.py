from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL, CASCADE

from django.utils.translation import gettext_lazy as _

from chess.chess_configurations import get_standard_chess_pieces

class GameType(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    rules = models.JSONField(default=get_standard_chess_pieces)
    created_by = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Game(models.Model):
    data = models.JSONField() # is the data used by the chess library

    @property
    def rules(self):
        return self.data['pieces']

    @property
    def board(self):
        return self.data['board']

    @property
    def turn(self):
        return self.data['players']['current']

    @property
    def turn_color(self):
        return self.data['players'][self.turn]['color']

    history = models.JSONField(null=True)
    player1 = models.ForeignKey(User, null=True, on_delete=CASCADE, related_name='games_player1')
    player2 = models.ForeignKey(User, null=True, on_delete=CASCADE, related_name='games_player2')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
