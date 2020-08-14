import pytest

from ..models import Game

class TestGame():
    def test_rules(self):
        game = Game()
        assert list(game.rules.keys()) == ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']

    def test_board(self):
        game = Game()
        pieces = ['pawn', 'knight', 'rook', 'bishop', 'king', 'queen']
        board = game.board
        assert list(board.keys()) == ['Player 1', 'Player 2']
        assert list(board['Player 1'].keys()) == pieces
        assert list(board['Player 2'].keys()) == pieces

    def test_turn(self):
        game = Game()
        assert game.turn == "Player 1"

    def test_color(self):
        game = Game()
        assert game.turn_color == "white"

    def test_rule_summary_no_summary(self):
        game = Game()
        assert None == game.rule_summary

    def test_rule_summary(self):
        game = Game()
        summary = {'name': "want some rule?"}
        game.data['rule_summary'] = summary
        assert summary == game.rule_summary
