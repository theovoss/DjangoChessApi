from django.forms import ModelForm, Textarea

from .models import Game, GameType


class GameTypeForm(ModelForm):
    class Meta:
        model = GameType
        fields = ['name', 'description']
        widgets = {
            'description': Textarea(attrs={'rows': 2, 'cols': 40}),
        }
