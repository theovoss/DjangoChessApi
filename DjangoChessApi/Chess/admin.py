from django.contrib import admin

from .models import Game, GameType


admin.site.register(GameType)
admin.site.register(Game)
