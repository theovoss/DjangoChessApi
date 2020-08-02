from rest_framework import serializers
from DjangoChessApi.Chess.models import GameType

class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameType
        fields = ['name', 'description', 'rules', 'created_by', 'created_at', 'updated_at']
