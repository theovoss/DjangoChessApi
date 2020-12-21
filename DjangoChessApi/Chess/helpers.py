from chess.chess_configurations import get_standard_chess_pieces


piece_images = {
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


def get_pieces(data, ignore=None):
    retval = {'black': {}, 'white': {}}
    normal_chess_rules = get_standard_chess_pieces()

    if data and 'pieces' in data:
        pieces = data['pieces']
    else:
        pieces = normal_chess_rules['pieces']

    for color in ['black', 'white']:
        for piece, piece_data in pieces.items():
            if ignore and piece in ignore:
                continue
            retval[color][piece] = {
                'image': _get_image(piece, color),
                'moves': piece_data['moves'],
            }

    return retval


def _get_image(piece, color):
    if piece in piece_images and color in piece_images[piece]:
        return piece_images[piece][color]
    return None


def _make_frontend_key(position):
    return "{},{}".format(*position)


def get_displayable_board(board):
    displayable = {}

    for position, piece in board.items():
        if not piece:
            displayable[_make_frontend_key(position)] = {}
        else:
            image = _get_image(piece.kind, piece.color)
            displayable[_make_frontend_key(position)] = {
                'image': image,
                'promote_me_daddy': piece.promote_me_daddy,
                'name': piece.kind,
                'color': piece.color,
            }
    return displayable


def get_displayable_history(chess):
    history = []
    internal_history = chess.get_history()
    for record in internal_history:
        displayable_name = _get_displayable_history_name(record['start'], record['end'])

        images = []
        class_name = ""
        if record.get('current'):
            class_name = "current"

        if 'captures' in record:
            recorded_captures = record['captures']
            for capture in recorded_captures:
                name = capture['name']
                color = capture['color']
                images.append(_get_image(name, color))

        history.append(
            {'name': displayable_name, 'images': images, 'class': class_name}
        )
    return history


def _get_displayable_history_name(_start, _end):
    start = _convert_to_external(_start)
    end = _convert_to_external(_end)
    return "{} -> {}".format(start, end)


def _convert_to_external(location):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    col = alphabet[location[1]]
    row = location[0] + 1
    return col + str(row)
