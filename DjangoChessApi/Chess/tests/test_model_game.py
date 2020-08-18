from django.test import TestCase

from ..models import Game


class TestGame(TestCase):
    def test_rules(self):
        game = Game()
        self.assertEqual(
            list(game.rules.keys()),
            ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king',],
        )

    def test_board(self):
        game = Game()
        pieces = ['pawn', 'knight', 'rook', 'bishop', 'king', 'queen']
        board = game.board
        self.assertEqual(list(board.keys()), ['Player 1', 'Player 2'])
        self.assertEqual(list(board['Player 1'].keys()), pieces)
        self.assertEqual(list(board['Player 2'].keys()), pieces)

    def test_turn(self):
        game = Game()
        self.assertEqual(game.turn, "Player 1")

    def test_color(self):
        game = Game()
        self.assertEqual(game.turn_color, "white")

    def test_rule_summary(self):
        game = Game(
            rule_name="want some rules?",
            rule_description="hey! this is descriptive! I swear!",
        )
        summary = {
            'name': 'want some rules?',
            'description': 'hey! this is descriptive! I swear!',
        }
        self.assertEqual(summary, game.rule_summary)
