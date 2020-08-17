from rest_framework import serializers

from DjangoChessApi.Chess.models import GameType


class GameTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameType
        fields = ['id', 'name', 'description', 'rules']
        read_only_fields = ['created_by', 'created_at', 'updated_at']
