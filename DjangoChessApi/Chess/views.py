from django.http import HttpResponse
from django.shortcuts import render

from chess.chess_configurations import *

import datetime

import log


def current_datetime(request):
    log.debug(request)
    now = datetime.datetime.now()
    html = ("<html><body>Welcome to DjangoChessApi."
            "<br>"
            "It is now %s.</body></html>") % now
    return HttpResponse(html)


def chess_configuration(request):
    log.debug(request)
    directions = get_movement_directions()
    movement_rules = get_movement_rules()
    capture_actions = get_capture_action_rules()

    context = {
        'pieces': {
            'King': {'image': 'https://upload.wikimedia.org/wikipedia/commons/f/f0/Chess_kdt45.svg'},
            'Queen': {'image': 'https://upload.wikimedia.org/wikipedia/commons/4/47/Chess_qdt45.svg'},
            'Knight': {'image': 'https://upload.wikimedia.org/wikipedia/commons/e/ef/Chess_ndt45.svg'},
            'Bishop': {'image': 'https://upload.wikimedia.org/wikipedia/commons/9/98/Chess_bdt45.svg'},
            'Rook': {'image': 'https://upload.wikimedia.org/wikipedia/commons/f/ff/Chess_rdt45.svg'},
            'Pawn': {'image': 'https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg'}
        },
        'directions': directions,
        'movements': movement_rules,
        'capture_actions': capture_actions
    }
    return render(request, 'chess/piece_configurations.html', context)