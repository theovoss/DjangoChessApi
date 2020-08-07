from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL, CASCADE

from django.utils.translation import gettext_lazy as _

from chess.chess_configurations import get_standard_chess_pieces

class GameType(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    rules = JSONField(default=get_standard_chess_pieces)
    created_by = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Game(models.Model):
    class Turn(models.TextChoices):
        BLACK = 'b', _('Black')
        WHITE = 'w', _('White')

    rules = JSONField()
    current_board = JSONField()
    turn = models.CharField(
        max_length=1,
        choices=Turn.choices,
        default=Turn.WHITE
    )

    history = JSONField(null=True)
    player1 = models.ForeignKey(User, null=True, on_delete=CASCADE, related_name='games_player1')
    player2 = models.ForeignKey(User, null=True, on_delete=CASCADE, related_name='games_player2')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
