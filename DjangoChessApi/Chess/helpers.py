from copy import deepcopy

from chess.chess_configurations import get_standard_chess_pieces


images = {
    'king': {
        'black': 'https://upload.wikimedia.org/wikipedia/commons/f/f0/Chess_kdt45.svg',
        'white': 'https://upload.wikimedia.org/wikipedia/commons/4/42/Chess_klt45.svg',
    },
    'queen': {
        'black': 'https://upload.wikimedia.org/wikipedia/commons/4/47/Chess_qdt45.svg',
        'white': 'https://upload.wikimedia.org/wikipedia/commons/1/15/Chess_qlt45.svg',
    },
    'knight': {
        'black': 'https://upload.wikimedia.org/wikipedia/commons/e/ef/Chess_ndt45.svg',
        'white': 'https://upload.wikimedia.org/wikipedia/commons/7/70/Chess_nlt45.svg',
    },
    'bishop': {
        'black': 'https://upload.wikimedia.org/wikipedia/commons/9/98/Chess_bdt45.svg',
        'white': 'https://upload.wikimedia.org/wikipedia/commons/b/b1/Chess_blt45.svg',
    },
    'rook': {
        'black': 'https://upload.wikimedia.org/wikipedia/commons/f/ff/Chess_rdt45.svg',
        'white': 'https://upload.wikimedia.org/wikipedia/commons/7/72/Chess_rlt45.svg',
    },
    'pawn': {
        'black': 'https://upload.wikimedia.org/wikipedia/commons/c/c7/Chess_pdt45.svg',
        'white': 'https://upload.wikimedia.org/wikipedia/commons/4/45/Chess_plt45.svg',
    },
}


def get_pieces(game_type, color):
    normal_chess_rules = get_standard_chess_pieces()

    if game_type.rules:
        pieces = game_type.rules['pieces']
    else:
        pieces = normal_chess_rules['pieces']

    for piece in pieces:
        pieces[piece]['image'] = get_image(piece, color)

    return deepcopy(pieces)


def get_image(piece, color):
    if piece in images and color in images[piece]:
        return images[piece][color]
    return None


def _make_frontend_key(position):
    return "{},{}".format(*position)


def get_displayable_board(board):
    displayable = {}

    for player in board:  # dict
        for piece in board[player]:  # dict
            color = 'white' if '1' in player else 'black'
            for data in board[player][piece]:  # List of dicts
                position = data['position']
                image = get_image(piece, color)
                displayable[_make_frontend_key(position)] = image
    return displayable


def get_displayable_history_name(_start, _end):
    start = _convert_to_external(_start)
    end = _convert_to_external(_end)
    return "{} -> {}".format(start, end)


def _convert_to_external(location):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    col = alphabet[location[1]]
    row = location[0] + 1
    return col + str(row)
