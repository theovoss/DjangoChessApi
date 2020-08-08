from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status

from chess.chess_configurations import get_movement_rules, \
                                       get_movement_directions, \
                                       get_capture_action_rules, \
                                       get_standard_chess_pieces

from DjangoChessApi.Chess.models import GameType
from ..serializers import GameTypeSerializer

class MovementViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(get_movement_rules())

class DirectionViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(get_movement_directions())

class CaptureActionViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(get_capture_action_rules())

class StandardChessPiecesViewSet(viewsets.ViewSet):
    def list(self, request):
        return Response(get_standard_chess_pieces())

class GameTypeViewSet(viewsets.ModelViewSet):
    serializer_class = GameTypeSerializer
    queryset = GameType.objects.all()

    def set_chess_data(self, initial_data, piece, index, key, values):
        if 'pieces' not in initial_data:
            initial_data['pieces'] = {}
        if piece not in initial_data['pieces']:
            initial_data['pieces'][piece] = {}

        piece = initial_data['pieces'][piece]

        if 'moves' in piece:
            if len(piece['moves']) <= index:
                piece['moves'].append({})
            individual_rule = piece['moves'][index]
        else:
            piece['moves'] = [{}]
            individual_rule = piece['moves'][index]

        individual_rule[key] = values

    def set_data(self, pk, piece, index, key, values):
        # Get model
        game_type = GameType.objects.get(pk=pk)

        # update path
        self.set_chess_data(game_type.rules, piece, index, key, values)

        # save model
        game_type.save()

    """
        input should be:
        {
            'piece': 'king',
            'index': '0',
            'key': 'directions', # or: 'conditions' or: 'capture_actions'
            'value': rule/direction/capture_actions
        }
    """
    def partial_update(self, request, pk=None):
        data = request.data
        data2 = dict(data)

        piece = data['piece']
        index = int(data['index'])
        key = data['key']
        values = data2['value'] # list of what are set

        # TODO: read up on serializers. might be able to replace these conditionals
        if key == 'directions':
            directions = get_movement_directions()
            for value in values:
                if value not in directions:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"Invalid action rule ERROR": "{} is not in {}".format(value, directions)})
            self.set_data(pk, piece, index, key, values)
        elif key == 'conditions':
            rules = get_movement_rules()
            for value in values:
                if value not in rules:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"Invalid action rule ERROR": "{} is not in {}".format(value, rules)})
            self.set_data(pk, piece, index, key, values)
        elif key == 'capture_actions':
            action_rules = get_capture_action_rules()
            for value in values:
                if value not in action_rules:
                    return Response(status=status.HTTP_400_BAD_REQUEST, data={"Invalid action rule ERROR": "{} is not in {}".format(value, action_rules)})
            self.set_data(pk, piece, index, key, values)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"Invalid key ERROR": "{} is not in ['conditions', 'capture_actions', or 'directions'".format(key)})

        return Response(status=status.HTTP_200_OK)
