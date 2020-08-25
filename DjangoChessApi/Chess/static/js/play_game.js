squares = document.querySelectorAll(".square");

// handle clicks
function gameClickHandler(e) {
  promoteable = document.querySelectorAll('.promote');
  if(promoteable.length > 0) {
    // don't allow additional moves while a piece is waiting to be promted.
    return;
  }
  otherSelected = document.querySelectorAll('.selected');
  currentDestinations = document.querySelectorAll('.destination');
  if(otherSelected.length == 0) {
    this.classList.toggle('selected');
    // call to get destinations and select those too.
    url = document.querySelector('.destinations_url').dataset.url;

    data = {
      row: this.dataset.row,
      column: this.dataset.column
    }

    const otherParams = getFetchParams(data);

    fetch(url, otherParams)
      .then(response => response.json())
      .then(data => {
        data.forEach(location => {
          row = location[0];
          column = location[1];

          div_id = document.getElementById(row + "," + column);
          div_id.classList.add('destination')
        })
      })
      .catch(error => console.log(error));
  } else {
    // if this is a destination, call move api
    if(this.classList.contains('destination')) {
      url = document.querySelector('.move_url').dataset.url;
      data = {
        destination: {
          row: this.dataset.row,
          column: this.dataset.column
        },
        start: {
          row: otherSelected[0].dataset.row,
          column: otherSelected[0].dataset.column
        }
      }
      const otherParams = getFetchParams(data);

      fetch(url, otherParams)
        .then(_ => location.reload())
        .catch(error => console.log(error));
    }
    // if this is not a destination, clear selections
    otherSelected.forEach(square => {
      square.classList.toggle('selected');
    });
    currentDestinations.forEach(square => {
      square.classList.toggle('destination');
    })
  }
}

squares.forEach(square => {
  square.addEventListener('click', gameClickHandler);
})