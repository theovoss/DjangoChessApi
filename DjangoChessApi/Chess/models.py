from django.db import models
from django.contrib.postgres.fields import JSONField
from django.contrib.auth.models import User
from django.db.models.deletion import SET_NULL

from chess.chess_configurations import get_standard_chess_pieces

class GameType(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    rules = JSONField(default=get_standard_chess_pieces)
    created_by = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
