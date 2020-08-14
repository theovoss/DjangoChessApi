import pprint

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from chess.chess import Chess

from DjangoChessApi.Chess.models import Game


class MoveViewSet(viewsets.ViewSet):
    def list(self, request, pk=None):
        return Response("Hey, gotta return somethin")

    @action(methods=['POST'], detail=True, url_name="destinations")
    def get_destinations(self, request, pk=None):
        game = Game.objects.get(pk=pk)
        chess = Chess(game.data)

        row = int(request.data['row'])
        column = int(request.data['column'])

        destinations = chess.destinations((row, column))
        return Response(destinations)

    @action(methods=['POST'], detail=True, url_name="move")
    def move(self, request, pk=None):
        game = Game.objects.get(pk=pk)

        chess = Chess(game.data)

        data = request.data
        destination_row = int(data['destination']['row'])
        destination_column = int(data['destination']['column'])
        start_row = int(data['start']['row'])
        start_column = int(data['start']['column'])

        chess.move((start_row, start_column), (destination_row, destination_column))

        # update db with new board
        game.data = chess.export()
        game.save()

        return Response("success, time to refresh")
