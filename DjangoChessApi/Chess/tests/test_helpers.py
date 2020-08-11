from DjangoChessApi.Chess.models import GameType
from DjangoChessApi.Chess.helpers import get_pieces, \
                                         get_image, \
                                         get_displayable_board


def test_get_pieces():
    game_type = GameType()

    assert game_type.rules is not None

    pieces = get_pieces(game_type, 'white')
    piece_names = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    assert list(pieces.keys()) == piece_names
    for move in pieces['pawn']['moves']:
        assert 'directions' in move
        assert 'conditions' in move

def test_get_pieces_no_game_type_rules():
    game_type = GameType()
    game_type.rules = None
    assert game_type.rules is None

    pieces = get_pieces(game_type, 'white')
    piece_names = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
    assert list(pieces.keys()) == piece_names
    for move in pieces['pawn']['moves']:
        assert 'directions' in move
        assert 'conditions' in move

def test_get_image_pawn():
    url = get_image('pawn', 'white')
    assert url == "https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg"

def test_get_image_non_existent_piece():
    url = get_image('thor', 'white')
    assert url == None

def test_get_image_non_existent_color():
    url = get_image('pawn', 'chartreuse')
    assert url == None

def test_get_displayable_board():
    game_type = GameType()

    actual = get_displayable_board(game_type.board)

    print("Keys are")
    print(actual.keys())
    for row in "0167":
        for column in range(8):
            key = "{},{}".format(row, column)
            assert ".svg" in actual[key]
