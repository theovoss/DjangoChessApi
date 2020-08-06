from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .models import GameType
from .forms import GameTypeForm

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


def chess_create_configuration(request):
    if request.method == "POST":
        form = GameTypeForm(request.POST)
        if form.is_valid():
            game_type = form.save()
            return HttpResponseRedirect("/configure/{}/".format(game_type.id))
    else:
        form = GameTypeForm()
    return render(request, 'chess/create_configuration.html', {'form': form})



def chess_configuration(request, game_type_id):
    game_type = GameType.objects.get(pk=game_type_id)

    if request.method == "POST":
        form = GameTypeForm(request.POST, instance=game_type)
        if form.is_valid():
            game_type = form.save()
    else:
        form = GameTypeForm(instance=game_type)

    log.debug(request)
    directions = get_movement_directions()
    movement_rules = get_movement_rules()
    capture_actions = get_capture_action_rules()
    normal_chess_rules = get_standard_chess_pieces()

    if game_type.rules:
        pieces = game_type.rules['pieces']
    else:
        pieces = normal_chess_rules['pieces']

    images = {
        'king': 'https://upload.wikimedia.org/wikipedia/commons/f/f0/Chess_kdt45.svg',
        'queen': 'https://upload.wikimedia.org/wikipedia/commons/4/47/Chess_qdt45.svg',
        'knight': 'https://upload.wikimedia.org/wikipedia/commons/e/ef/Chess_ndt45.svg',
        'bishop': 'https://upload.wikimedia.org/wikipedia/commons/9/98/Chess_bdt45.svg',
        'rook': 'https://upload.wikimedia.org/wikipedia/commons/f/ff/Chess_rdt45.svg',
        'pawn': 'https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg'
    }

    for piece in pieces:
        if piece in images:
            pieces[piece]['image'] = images[piece]

    context = {
        'id': game_type.id,
        'pieces': pieces,
        'directions': directions,
        'movements': movement_rules,
        'capture_actions': capture_actions,
        'form': form
    }
    return render(request, 'chess/piece_configurations.html', context)