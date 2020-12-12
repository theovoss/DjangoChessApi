import pprint

from chess.chess import Chess
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from DjangoChessApi.Chess.models import Game


class MoveViewSet(viewsets.ViewSet):
    @action(methods=['POST'], detail=True, url_name="promote")
    def promote(self, request, pk=None):
        game = Game.objects.get(pk=pk)
        if not game.is_my_turn(request.user):
            return Response("not your turn", status=status.HTTP_400_BAD_REQUEST)
        chess = Chess(game.data)

        chess.promote(
            (request.data['row'], request.data['column']), request.data['name']
        )

        # update db with new board
        game.data = chess.export()
        game.save()

        return Response("success, time to refresh")

    @action(methods=['POST'], detail=True, url_name="destinations")
    def get_destinations(self, request, pk=None):
        game = Game.objects.get(pk=pk)
        if game.ready_to_play:
            chess = Chess(game.data)

            row = int(request.data['row'])
            column = int(request.data['column'])

            destinations = chess.destinations((row, column))
            return Response(destinations)
        return Response("not your turn", status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['POST'], detail=True, url_name="move")
    def move(self, request, pk=None):
        game = Game.objects.get(pk=pk)
        if not game.is_my_turn(request.user):
            return Response("not your turn", status=status.HTTP_400_BAD_REQUEST)

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
