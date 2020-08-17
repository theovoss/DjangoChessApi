from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action

from chess.chess import Chess

from DjangoChessApi.Chess.models import Game


class HistoryViewSet(viewsets.ViewSet):
    @action(methods=['POST'], detail=True, url_name="previous")
    def previous(self, request, pk=None):
        game = Game.objects.get(pk=pk)

        chess = Chess(game.data)

        chess._board.previous()

        # update db with new board
        game.data = chess.export()
        game.save()
        return Response("success, time to refresh")

    @action(methods=['POST'], detail=True, url_name="next")
    def next(self, request, pk=None):
        game = Game.objects.get(pk=pk)

        chess = Chess(game.data)

        chess._board.next()

        # update db with new board
        game.data = chess.export()
        game.save()
        return Response("success, time to refresh")

    @action(methods=['POST'], detail=True, url_name="first")
    def first(self, request, pk=None):
        game = Game.objects.get(pk=pk)

        chess = Chess(game.data)

        chess._board.first()

        # update db with new board
        # TODO: how to navigate history without changing current state?
        # TODO: how to differentiate a takeback vs seeing a previous board state?
        game.data = chess.export()
        game.save()
        return Response("success, time to refresh")