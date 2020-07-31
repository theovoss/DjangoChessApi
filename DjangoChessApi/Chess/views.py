from django.http import HttpResponse
from django.shortcuts import render

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
    context = {
        'pieces': {
            'King': {'image': 'https://upload.wikimedia.org/wikipedia/commons/f/f0/Chess_kdt45.svg'},
            'Queen': {'image': 'https://upload.wikimedia.org/wikipedia/commons/4/47/Chess_qdt45.svg'},
            'Knight': {'image': 'https://upload.wikimedia.org/wikipedia/commons/e/ef/Chess_ndt45.svg'},
            'Bishop': {'image': 'https://upload.wikimedia.org/wikipedia/commons/9/98/Chess_bdt45.svg'},
            'Rook': {'image': 'https://upload.wikimedia.org/wikipedia/commons/f/ff/Chess_rdt45.svg'},
            'Pawn': {'image': 'https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg'}
        },
        'directions': ['Vertical', 'Horizontal', 'Diagonal', 'L Shape'],
        'movements': ['distance_of_one', 'directional', 'cant_jump_pieces', 'ends_on_enemy']
    }
    return render(request, 'chess/piece_configurations.html', context)