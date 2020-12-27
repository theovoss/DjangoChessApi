# pylint: disable=E1136
# disabling E1136 so pylint doesn't yell about indexing json fields
import random
from enum import Enum

from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL

from chess.chess_configurations import get_standard_chess_pieces


class VisibilityOptions(Enum):
    PRIVATE = "PR"
    FRIENDS = "FR"
    PUBLIC = "PU"
    STANDARD = "ST"

    @classmethod
    def all(cls):
        return [
            VisibilityOptions.PRIVATE,
            VisibilityOptions.FRIENDS,
            VisibilityOptions.PUBLIC,
            VisibilityOptions.STANDARD,
        ]


class GameType(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    rules = models.JSONField(default=get_standard_chess_pieces)
    visibility = models.CharField(
        default=VisibilityOptions.PRIVATE.value,
        max_length=2,
        choices=[(tag.value, tag.name) for tag in VisibilityOptions.all()],
    )
    created_by = models.ForeignKey(User, null=True, on_delete=SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def rule_definitions(self):
        return self.rules['pieces']

    def get_rules(self):
        return self.rules

    def player_for_color(self, color):
        for player in self.rules['players'].keys():
            if player != 'current' and self.rules['players'][player]['color'] == color:
                return player
        return None

    def set_piece_location(self, player, piece_name, row, column):
        self.clear_location(row, column)
        self.rules['board'][player][piece_name].append(
            {'position': [row, column], 'move_count': 0}
        )

    def clear_location(self, row, column):
        for player in self.rules['board']:
            for piece in self.rules['board'][player]:
                for definition in self.rules['board'][player][piece]:
                    if definition['position'] == [row, column]:
                        self.rules['board'][player][piece].remove(definition)
                        return


class Game(models.Model):
    data = models.JSONField(
        default=get_standard_chess_pieces
    )  # is the data used by the chess library

    rule_name = models.CharField(max_length=30)
    rule_description = models.TextField()

    free_play = models.BooleanField(default=True)  # if set to true, don't enforce users for white/black

    history = models.JSONField(null=True)
    player1 = models.ForeignKey(
        User, null=True, on_delete=CASCADE, related_name='games_player1'
    )
    player2 = models.ForeignKey(
        User, null=True, on_delete=CASCADE, related_name='games_player2'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def has_both_players(self):
        return self.player1 is not None and self.player2 is not None

    @property
    def ready_to_play(self):
        return self.free_play if self.free_play else self.has_both_players

    @property
    def rules(self):
        return self.data['pieces']

    @property
    def turn(self):
        return self.data['players']['current']

    def is_my_turn(self, user):
        if not self.ready_to_play:
            return False
        elif self.free_play:
            return True
        elif self.data['players']['current'] == 'Player 1':
            return user == self.player1
        else:
            return user == self.player2

    @property
    def turn_color(self):
        return self.data['players'][self.turn]['color']

    @property
    def rule_summary(self):
        return {'name': self.rule_name, 'description': self.rule_description}

    def set_player(self, user, color):
        if user.is_authenticated:
            if color == 'random':
                if random.choice([1, 2]) == 1:
                    self.player1 = user
                else:
                    self.player2 = user
            elif color == 'white' and self.player1 is None:
                self.player1 = user
            elif color == 'black' and self.player2 is None:
                self.player2 = user
            else:
                print("somehow don't know who to set??")

    def set_player2(self, user):
        if self.player1 is None and self.player2 != user:
            self.player1 = user
        elif self.player2 is None and self.player1 != user:
            self.player2 = user
        else:
            print("Setting second player but already set or existing player.")
