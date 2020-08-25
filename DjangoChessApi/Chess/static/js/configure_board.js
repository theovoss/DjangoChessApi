pieces = document.querySelectorAll('.card');
squares = document.querySelectorAll('.square');

pieces.forEach(piece => {
  piece.addEventListener("click", () => {
    pieces.forEach(other_piece => {
      if(piece === other_piece) {
        piece.classList.toggle('selected');
      } else {
        other_piece.classList.remove('selected');
      }
    });
  });
});

function setSquare(square) {
  piece = document.querySelector('.card.selected img');
  column = square.dataset.column;
  row = square.dataset.row;
  piece_name = null
  color = null
  if(piece) {
    parent = piece.parentElement;
    piece_name = parent.dataset.piece;
    color = parent.dataset.color;
  }
  // post data about square and piece to api.
  url = document.querySelector('.url').dataset.url;

  while(square.firstChild) {
    square.removeChild(square.lastChild);
  }
  if(piece) {
    square.append(piece.cloneNode());
  }

  data = {
    'row': row,
    'column': column,
    'piece': piece_name,
    'color': color
  }

  const otherParams = getFetchParams(data);

  // TODO: Handle responses somehow. Maybe on 400/500 uncheck the box since it didn't save, and maybe show an error...
  fetch(url, otherParams)
    .then(response => console.log(response))
    .catch(error => console.log(error));
}

squares.forEach(square => {
  square.addEventListener('mouseover', (event) => {
    if(event.shiftKey) {
      console.log("Setting square");
      setSquare(square);
    }
  });
  square.addEventListener("click", () => {
    console.log("Setting square");
    setSquare(square);
  });
});