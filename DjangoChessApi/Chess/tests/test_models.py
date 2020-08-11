import pytest

from ..models import GameType


def test_can_import_chess_library():
    from chess.chess import Chess
    chess = Chess()


@pytest.mark.django_db
def test_game_type_model_can_save():
    initial_total = len(GameType.objects.all())
    gt = GameType(name="hello", description="goodbye")
    gt.save()

    final_total = len(GameType.objects.all())
    assert(initial_total + 1 == final_total)
    gt.delete()


def test_game_type_clear_location():
    gt = GameType(name="hello", description="goodbye")

    testing_position = {'position': [1, 0], 'move_count': 0}
    assert(testing_position in gt.rules['board']['Player 1']['pawn'])

    gt.clear_location(1, 0)

    assert(testing_position not in gt.rules['board']['Player 1']['pawn'])


def test_game_type_set_location():
    gt = GameType(name="hello", description="goodbye")

    testing_position = {'position': [1, 0], 'move_count': 0}
    assert(testing_position in gt.rules['board']['Player 1']['pawn'])

    gt.set_piece_location('Player 1', 'knight', 1, 0)

    assert(testing_position not in gt.rules['board']['Player 1']['pawn'])
    assert(testing_position in gt.rules['board']['Player 1']['knight'])
