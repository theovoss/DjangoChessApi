from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from rest_framework.reverse import reverse

from chess.chess import Chess

from .models import GameType, Game
from .forms import GameTypeForm
from .helpers import get_image, get_displayable_board, get_pieces, get_displayable_history_name

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
    new_game = Game(data=game_type.get_rules())
    new_game.save()
    url = reverse('Chess:play-game', kwargs={'game_id': new_game.id})
    return HttpResponseRedirect(url)


def _get_displayable_history(game):
    chess = Chess(game.data)
    history = []
    # TODO: modify chess to expose these things we need.
    internal_history = chess._board._history._history
    index = chess._board._history._index
    for num, record in enumerate(internal_history):
        start = record['start']
        end = record['end']
        displayable_name = get_displayable_history_name(start, end)

        image = ""
        class_name = ""
        if num == index:
            class_name = "current"

        if 'captures' in record:
            recorded_captures = record['captures']
            if len(recorded_captures) > 1:
                print("Captured multiple... now what??")
            for capture in recorded_captures:
                name = capture['name']
                color = capture['color']
                image = get_image(name, color)

        history.append({'name': displayable_name, 'image': image, 'class': class_name})
    return history


def play_game(request, game_id):
    game = Game.objects.get(pk=game_id)

    displayable_board = get_displayable_board(game.board)
    destinations_url = reverse('move-destinations', args=[game.id])
    move_url = reverse('move-move', args=[game.id])

    history = _get_displayable_history(game)
    context = {
        'board': displayable_board,
        'destinations_url': destinations_url,
        'move_url': move_url,
        'rule_summary': game.rule_summary,
        'turn': game.turn_color,
        'history': history,
        'id': game.id
    }
    return render(request, 'chess/main/play_game.html', context)


def create_configuration(request):
    if request.method == "POST":
        form = GameTypeForm(request.POST)
        if form.is_valid():
            game_type = form.save()
            return HttpResponseRedirect(reverse('Chess:configure-edit', kwargs={'game_type_id': game_type.id}))
    else:
        form = GameTypeForm()
    return render(request, 'chess/main/create_configuration.html', {'form': form})

def configuration_board(request, game_type_id):
    game_type = GameType.objects.get(pk=game_type_id)
    displayable_board = get_displayable_board(game_type.board)

    if request.method == "POST":
        form = GameTypeForm(request.POST, instance=game_type)
        if form.is_valid():
            game_type = form.save()
    else:
        form = GameTypeForm(instance=game_type)

    black_pieces = get_pieces(game_type, "black")
    white_pieces = get_pieces(game_type, "white")
    url = reverse('chess-configuration-configure-board', args=[game_type.id])

    context = {
        'id': game_type.id,
        'form': form,
        'board': displayable_board,
        'black_pieces': black_pieces,
        'white_pieces': white_pieces,
        'url': url
    }
    return render(request, 'chess/main/configure_board.html', context)


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

    pieces = get_pieces(game_type, "black")

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
