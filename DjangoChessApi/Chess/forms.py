from django.forms import ModelForm
from .models import GameType

class GameTypeForm(ModelForm):
    class Meta:
        model = GameType
        fields = ['name', 'description']
