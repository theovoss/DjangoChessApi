from django.test import SimpleTestCase

from DjangoChessApi.Chess.helpers import get_displayable_board, get_image, get_pieces
from DjangoChessApi.Chess.models import GameType


class TestGetPieces(SimpleTestCase):
    def test_get_pieces(self):
        game_type = GameType()

        self.assertIsNotNone(game_type.rules)

        pieces = get_pieces(game_type, 'white')
        piece_names = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        self.assertEqual(list(pieces.keys()), piece_names)
        for move in pieces['pawn']['moves']:
            self.assertIn('directions', move)
            self.assertIn('conditions', move)

    def test_get_pieces_no_game_type_rules(self):
        game_type = GameType()
        game_type.rules = None
        self.assertIsNone(game_type.rules, None)

        pieces = get_pieces(game_type, 'white')
        piece_names = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        self.assertEqual(list(pieces.keys()), piece_names)
        for move in pieces['pawn']['moves']:
            self.assertIn('directions', move)
            self.assertIn('conditions', move)


class TestGetImage(SimpleTestCase):
    def test_get_image_pawn(self):
        url = get_image('pawn', 'white')
        self.assertEqual(
            url, "https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg"
        )

    def test_get_image_non_existent_piece(self):
        url = get_image('thor', 'white')
        self.assertIsNone(url)

    def test_get_image_non_existent_color(self):
        url = get_image('pawn', 'chartreuse')
        self.assertIsNone(url)


class TestGetDisplayableBoard(SimpleTestCase):
    def test_get_displayable_board(self):
        game_type = GameType()

        actual = get_displayable_board(game_type.board)

        for row in "0167":
            for column in range(8):
                key = "{},{}".format(row, column)
                self.assertIn(".svg", actual[key])
