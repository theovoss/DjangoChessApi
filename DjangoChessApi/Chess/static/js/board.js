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