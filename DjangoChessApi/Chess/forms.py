from django.forms import ModelForm
from .models import GameType, Game

class GameTypeForm(ModelForm):
    class Meta:
        model = GameType
        fields = ['name', 'description']

# class CreateGameForm(Form):
#     Form.