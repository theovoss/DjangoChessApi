from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from rest_framework.reverse import reverse

from .models import GameType, Game
from .forms import GameTypeForm
from .helpers import get_image, get_displayable_board

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


def home(request):
    game_types = GameType.objects.all()
    return render(request, 'chess/main/home.html', {'game_types': game_types})


def create_game(request):
    game_types = GameType.objects.all()
    return render(request, 'chess/main/create_game.html', {'game_types': game_types})


def create_game_redirect(request, game_type_id):
    game_type = GameType.objects.get(pk=game_type_id)
    new_game = Game(data=game_type.rules)
    new_game.save()
    url = reverse('Chess:play-game', kwargs={'game_id': new_game.id})
    return HttpResponseRedirect(url)


def play_game(request, game_id):
    game = Game.objects.get(pk=game_id)
    name = "hardcoded for now"
    displayable_board = get_displayable_board(game.board)
    destinations_url = reverse('move-destinations', args=[game.id])
    move_url = reverse('move-move', args=[game.id])
    return render(request, 'chess/main/play_game.html', {
        'name': name,
        'board': displayable_board,
        'destinations_url': destinations_url,
        'move_url': move_url
    })


def create_configuration(request):
    if request.method == "POST":
        form = GameTypeForm(request.POST)
        if form.is_valid():
            game_type = form.save()
            return HttpResponseRedirect(reverse('configure', game_type.id))
    else:
        form = GameTypeForm()
    return render(request, 'chess/main/create_configuration.html', {'form': form})


def configuration(request, game_type_id):
    game_type = GameType.objects.get(pk=game_type_id)

    if request.method == "POST":
        form = GameTypeForm(request.POST, instance=game_type)
        if form.is_valid():
            game_type = form.save()
    else:
        form = GameTypeForm(instance=game_type)

    directions = get_movement_directions()
    movement_rules = get_movement_rules()
    capture_actions = get_capture_action_rules()
    normal_chess_rules = get_standard_chess_pieces()

    if game_type.rules:
        pieces = game_type.rules['pieces']
    else:
        pieces = normal_chess_rules['pieces']

    for piece in pieces:
        pieces[piece]['image'] = get_image(piece, 'black')

    checkmark_url = reverse('chess-configuration-checkmark', args=[game_type.id])

    context = {
        'id': game_type.id,
        'checkmark_url': checkmark_url,
        'pieces': pieces,
        'enums': {
            'directions': directions,
            'movements': movement_rules,
            'capture_actions': capture_actions
        },
        'form': form
    }
    return render(request, 'chess/main/configuration.html', context)
