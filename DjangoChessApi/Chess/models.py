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

    @property
    def rule_definitions(self):
        return self.rules['pieces']

    @property
    def board(self):
        return self.rules['board']

    def get_rules(self):
        rules = self.rules
        rules['rule_summary'] = {
            'name': self.name,
            'description': self.description
        }
        return rules


    def player_for_color(self, color):
        for player in self.rules['players'].keys():
            if player != 'current' and self.rules['players'][player]['color'] == color:
                return player

    def set_piece_location(self, player, piece_name, row, column):
        self.clear_location(row, column)
        self.rules['board'][player][piece_name].append({
            'position': [row, column],
            'move_count': 0
        })

    def clear_location(self, row, column):
        for player in self.rules['board']:
            for piece in self.rules['board'][player]:
                for definition in self.rules['board'][player][piece]:
                    if definition['position'] == [row, column]:
                        self.rules['board'][player][piece].remove(definition)
                        return

class Game(models.Model):
    data = models.JSONField(default=get_standard_chess_pieces) # is the data used by the chess library

    history = models.JSONField(null=True)
    player1 = models.ForeignKey(User, null=True, on_delete=CASCADE, related_name='games_player1')
    player2 = models.ForeignKey(User, null=True, on_delete=CASCADE, related_name='games_player2')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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

    @property
    def rule_summary(self):
        return self.data.get('rule_summary')
