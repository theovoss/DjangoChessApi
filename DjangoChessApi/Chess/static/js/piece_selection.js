promote_pieces = document.querySelectorAll('.promote');

promote_template_black = document.getElementById('piece-selection-popover-content-black')
promote_template_white = document.getElementById('piece-selection-popover-content-white')

// set bootstrap popover data attributes
let attributes = {
  'placement': 'right',
  'toggle': 'popover',
  'container': 'body',
  'trigger': 'manual',
  'html': true
}

$('.promote').data(attributes)

// initialize and manually show the popover (can't be dismissed)
$('.promote').popover({
  container: 'body',
  title: 'Promote',
  content: function() {
    color = this.dataset.color;
    template = $(`#piece-selection-popover-content-${color}`).html()
    return template;
  }
});

$('.promote').popover('show');

function select_piece(event) {
  piece_name = this.getElementsByTagName('img')[0].alt;

  popover_id = this.parentElement.parentElement.id;
  attached_piece = $(`[aria-describedby="${popover_id}"`)[0];

  row = attached_piece.dataset.row;
  column = attached_piece.dataset.column;

  data = {
    'row': parseInt(row),
    'column': parseInt(column),
    'name': piece_name,
  }

  url = document.querySelector('.promote_url').dataset.url;

  const otherParams = getFetchParams(data);

  fetch(url, otherParams)
    .then(response => location.reload())
    .catch(error => console.log(error));
}

$('.popover-body .card').click(select_piece);
