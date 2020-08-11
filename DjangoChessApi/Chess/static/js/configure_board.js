pieces = document.querySelectorAll('.card');
squares = document.querySelectorAll('.square');

pieces.forEach(piece => {
  piece.addEventListener("click", () => {
    console.log("In event handler");
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
  // square.dataset.column;
  // square.dataset.row;
  // piece.dataset.piece;
  // piece.dataset.color;
  // post data about square and piece to api.
  while(square.firstChild) {
    square.removeChild(square.lastChild);
  }
  square.append(piece.cloneNode());
}

squares.forEach(square => {
  square.addEventListener('mouseover', (event) => {
    if(event.shiftKey) {
      setSquare(square);
    }
  });
  square.addEventListener("click", () => {
    setSquare(square);
  });
});