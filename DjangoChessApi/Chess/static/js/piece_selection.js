export default promote_check;

function promote_check() {
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
      var color = this.dataset.color;
      var template = $(`#piece-selection-popover-content-${color}`).html()
      return template;
    }
  });

  $('.promote').popover('show');

  function select_piece(event) {
    var piece_name = this.getElementsByTagName('img')[0].alt;

    var popover_id = this.parentElement.parentElement.id;
    var attached_piece = $(`[aria-describedby="${popover_id}"`)[0];

    var row = attached_piece.dataset.row;
    var column = attached_piece.dataset.column;

    var data = {
      'row': parseInt(row),
      'column': parseInt(column),
      'name': piece_name,
    }

    var url = document.querySelector('.promote_url').dataset.url;

    const otherParams = getFetchParams(data);

    fetch(url, otherParams)
      .then(response => location.reload())
      .catch(error => console.log(error));
  }

  $('.popover-body .card').click(select_piece);
}

promote_check();
