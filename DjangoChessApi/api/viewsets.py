from rest_framework import viewsets
from rest_framework.response import Response

from chess.chess_configurations import get_movement_rules, \
                                       get_movement_directions, \
                                       get_capture_action_rules

from DjangoChessApi.Chess.models import GameType
from .serializers import GameTypeSerializer

class MovementViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(get_movement_rules())

class DirectionViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(get_movement_directions())

class CaptureActionViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(get_capture_action_rules())

class GameSettingsViewSet(viewsets.ViewSet):
    def create(self, request, pk=None):
        print(request.data)
        print(pk)
        return Response(["successfuly called create"])

    def update(self, request, pk=None):
        print(request.data)
        print(pk)
        return Response(["successfuly called update"])

class GameTypeViewSet(viewsets.ModelViewSet):
    serializer_class = GameTypeSerializer
    queryset = GameType.objects.all()
