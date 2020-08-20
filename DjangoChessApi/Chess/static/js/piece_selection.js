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
  content: function() {
    return $('#piece-selection-popover-content-black').html();
  }
});

$('.promote').popover('show');



