squares = document.querySelectorAll(".square");


// Initialize Board
function isOdd(num) {
  return num % 2;
}

function odnessMatches(num1, num2) {
  return isOdd(num1) === isOdd(num2);
}

squares.forEach(square => {
  row = square.dataset.row;
  column = square.dataset.column;

  if(odnessMatches(row, row + column)) {
    square.classList.add('dark');
  } else {
    square.classList.add('light');
  }
});

// handle clicks
function clickHandler(e) {
  console.log(e);
  otherSelected = document.querySelectorAll('.selected');
  if(otherSelected.length == 0) {
    this.classList.toggle('selected');
    // call to get destinations and select those too.
  } else {
    // if this is a destination, call move api
    // if this is not a destination, clear selections
    otherSelected.forEach(square => {
      square.classList.toggle('selected');
    });
  }
  console.log(this);
}

squares.forEach(square => {
  square.addEventListener('click', clickHandler);
})