import pytest

from ..models import GameType


def test_can_import_chess_library():
    from chess.chess import Chess
    Chess()

class TestGameType():
    @pytest.mark.django_db
    def test_model_can_save(self):
        initial_total = len(GameType.objects.all())
        gt = GameType(name="hello", description="goodbye")
        gt.save()

        final_total = len(GameType.objects.all())
        assert(initial_total + 1 == final_total)
        gt.delete()

    def test_rule_definitions(self):
        gt = GameType()
        actual = gt.rule_definitions
        assert gt.rules['pieces'] == actual

    def test_player_for_color(self):
        gt = GameType()
        white = gt.player_for_color('white')
        assert 'Player 1' == white

        black = gt.player_for_color('black')
        assert 'Player 2' == black

        actual = gt.player_for_color('actual')
        assert None == actual

    def test_clear_location(self):
        gt = GameType(name="hello", description="goodbye")

        testing_position = {'position': [1, 0], 'move_count': 0}
        assert(testing_position in gt.rules['board']['Player 1']['pawn'])

        gt.clear_location(1, 0)

        assert(testing_position not in gt.rules['board']['Player 1']['pawn'])

    def test_clear_location_invalid_location(self):
        gt = GameType(name="hello", description="goodbye")

        gt.clear_location(-1, 0)
        # testing this doesn't cause index errors

    def test_set_location(self):
        gt = GameType(name="hello", description="goodbye")

        testing_position = {'position': [1, 0], 'move_count': 0}
        assert(testing_position in gt.rules['board']['Player 1']['pawn'])

        gt.set_piece_location('Player 1', 'knight', 1, 0)

        assert(testing_position not in gt.rules['board']['Player 1']['pawn'])
        assert(testing_position in gt.rules['board']['Player 1']['knight'])
