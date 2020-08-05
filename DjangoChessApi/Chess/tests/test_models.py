import pytest

from ..models import GameType

def test_placeholder():
    pass

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
