from django.test import SimpleTestCase

from chess.chess import Chess

from DjangoChessApi.Chess.helpers import (
    _get_image,
    get_displayable_board,
    get_displayable_history,
    get_pieces,
)
from DjangoChessApi.Chess.models import GameType


class TestGetPieces(SimpleTestCase):
    def test_get_pieces(self):
        game_type = GameType()

        self.assertIsNotNone(game_type.rules)

        pieces = get_pieces(game_type.rules)['white']
        piece_names = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        self.assertEqual(list(pieces.keys()), piece_names)
        for move in pieces['pawn']['moves']:
            self.assertIn('directions', move)
            self.assertIn('conditions', move)

    def test_get_pieces_ignoring_some(self):
        game_type = GameType()

        self.assertIsNotNone(game_type.rules)

        pieces = get_pieces(game_type.rules, ['king', 'pawn'])['white']
        piece_names = ['rook', 'knight', 'bishop', 'queen']
        self.assertEqual(list(pieces.keys()), piece_names)
        for move in pieces['bishop']['moves']:
            self.assertIn('directions', move)
            self.assertIn('conditions', move)

    def test_get_pieces_no_game_type_rules(self):
        pieces = get_pieces(None)['white']
        piece_names = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        self.assertEqual(list(pieces.keys()), piece_names)
        for move in pieces['pawn']['moves']:
            self.assertIn('directions', move)
            self.assertIn('conditions', move)


class TestGetImage(SimpleTestCase):
    def test_get_image_pawn(self):
        url = _get_image('pawn', 'white')
        self.assertEqual(
            url, "https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg"
        )

    def test_get_image_non_existent_piece(self):
        url = _get_image('thor', 'white')
        self.assertIsNone(url)

    def test_get_image_non_existent_color(self):
        url = _get_image('pawn', 'chartreuse')
        self.assertIsNone(url)


class TestGetDisplayableBoard(SimpleTestCase):
    def test_get_displayable_board(self):
        chess = Chess()

        actual = get_displayable_board(chess.board)

        for row in "0167":
            for column in range(8):
                key = "{},{}".format(row, column)
                self.assertIn(".svg", actual[key]['image'])


class TestGetDisplayablehistory(SimpleTestCase):
    def test_get_displayable_history_empty(self):
        chess = Chess()

        actual = get_displayable_history(chess)

        self.assertEqual(actual, [])

    def test_get_displayable_history_no_capture_history(self):
        chess = Chess()
        chess.move((1, 1), (2, 1))
        chess.move((6, 4), (5, 4))
        chess.move((2, 1), (3, 1))

        actual = get_displayable_history(chess)

        self.assertEqual(
            actual,
            [
                {'name': 'b2 -> b3', 'images': [], 'class': ''},
                {'name': 'e7 -> e6', 'images': [], 'class': ''},
                {'name': 'b3 -> b4', 'images': [], 'class': 'current'},
            ],
        )

    def test_get_displayable_history_with_capture_history(self):
        chess = Chess()
        chess.move((1, 1), (3, 1))
        chess.move((6, 2), (4, 2))
        chess.move((3, 1), (4, 2))

        actual = get_displayable_history(chess)

        self.assertEqual(
            actual,
            [
                {'name': 'b2 -> b4', 'images': [], 'class': ''},
                {'name': 'c7 -> c5', 'images': [], 'class': ''},
                {
                    'name': 'b4 -> c5',
                    'images': [
                        'https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg'
                    ],
                    'class': 'current',
                },
            ],
        )
