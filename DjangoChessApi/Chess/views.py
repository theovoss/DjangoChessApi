import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

import log
from chess.chess import Chess
from chess.chess_configurations import (
    get_capture_action_rules,
    get_movement_directions,
    get_movement_rules,
    get_post_move_actions_rules,
)
from rest_framework.reverse import reverse

from .forms import GameTypeForm
from .helpers import get_displayable_board, get_displayable_history, get_pieces
from .models import Game, GameType


def current_datetime(request):
    log.debug(request)
    now = datetime.datetime.now()
    html = (
        "<html><body>Welcome to DjangoChessApi." "<br>" "It is now %s.</body></html>"
    ) % now
    return HttpResponse(html)


def home(request):
    game_types = GameType.objects.all()
    return render(request, 'chess/main/home.html', {'game_types': game_types})


def create_game(request):
    game_types = GameType.objects.all()
    return render(request, 'chess/main/create_game.html', {'game_types': game_types})


def create_game_redirect(_, game_type_id):
    game_type = GameType.objects.get(pk=game_type_id)
    new_game = Game(
        data=game_type.get_rules(),
        rule_name=game_type.name,
        rule_description=game_type.description,
    )
    new_game.save()
    url = reverse('Chess:play-game', kwargs={'game_id': new_game.id})
    return HttpResponseRedirect(url)


def play_game(request, game_id):
    game = Game.objects.get(pk=game_id)
    chess = Chess(game.data)
    displayable_board = get_displayable_board(chess.board)
    destinations_url = reverse('move-destinations', args=[game.id])
    move_url = reverse('move-move', args=[game.id])
    promote_url = reverse('move-promote', args=[game.id])

    promotion_pieces = get_pieces(game.data, ignore=['king', 'pawn'])

    history = get_displayable_history(chess)
    context = {
        'board': displayable_board,
        'destinations_url': destinations_url,
        'move_url': move_url,
        'promote_url': promote_url,
        'rule_summary': game.rule_summary,
        'turn': game.turn_color,
        'history': history,
        'id': game.id,
        'promotion_pieces': promotion_pieces,
    }
    return render(request, 'chess/main/play_game.html', context)


def create_configuration(request):
    if request.method == "POST":
        form = GameTypeForm(request.POST)
        if form.is_valid():
            game_type = form.save()
            return HttpResponseRedirect(
                reverse('Chess:configure-edit', kwargs={'game_type_id': game_type.id})
            )
    else:
        form = GameTypeForm()
    return render(request, 'chess/main/create_configuration.html', {'form': form})


def configuration_board(request, game_type_id):
    game_type = GameType.objects.get(pk=game_type_id)
    chess = Chess(game_type.rules)
    displayable_board = get_displayable_board(chess.board)

    if request.method == "POST":
        form = GameTypeForm(request.POST, instance=game_type)
        if form.is_valid():
            game_type = form.save()
    else:
        form = GameTypeForm(instance=game_type)

    pieces = get_pieces(game_type.rules)

    url = reverse('chess-configuration-configure-board', args=[game_type.id])

    context = {
        'id': game_type.id,
        'form': form,
        'board': displayable_board,
        'black_pieces': pieces['black'],
        'white_pieces': pieces['white'],
        'url': url,
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
    post_move_actions = get_post_move_actions_rules()
    pieces = get_pieces(game_type.rules)['black']

    checkmark_url = reverse('chess-configuration-checkmark', args=[game_type.id])

    context = {
        'id': game_type.id,
        'checkmark_url': checkmark_url,
        'pieces': pieces,
        'enums': {
            'directions': directions,
            'movements': movement_rules,
            'capture_actions': capture_actions,
            'post_move_actions': post_move_actions,
        },
        'form': form,
    }
    return render(request, 'chess/main/configuration.html', context)
