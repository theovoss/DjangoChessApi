squares = document.querySelectorAll(".square");

game_id =  document.getElementById('game_id').dataset.id;

var prefix = 'wss://';
if (location.protocol !== 'https:') {
  prefix = 'ws://';
}
const chatSocket = new WebSocket(
  prefix
  + window.location.host
  + '/ws/chat/'
  + game_id
  + '/'
);

chatSocket.onmessage = function(e) {
  const data = JSON.parse(e.data);
  console.log(data);
  updateBoard(data.board);
  updateHistory(data.history);
  updateCurrentPlayer(data.color);
};

function updateCurrentPlayer(color) {
  console.log("Updating current player");
  elem = document.getElementById('turn');
  elem.innerText = capitalizeFirstLetter(color) + "'s Turn";
}

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function updateHistory(history_json) {
  console.log("Updating history");
  // update all history
  elem = document.getElementById("history-content");
  elem.innerHTML = '';
  history_json.forEach(item => {
    var hist_elem = getHistoryItem(item);
    elem.appendChild(hist_elem);
  });
  elem.scrollTop = elem.scrollHeight;
}

function updateBoard(board_json, start=null, destination=null) {
  console.log("Updating board")
  // update everything
  for (const [key, value] of Object.entries(board_json)) {
    setImage(key, value.image);
  }
}

function getHistoryItem(item) {
  let elem = document.createElement("p");
  var t = document.createTextNode(item.name);
  elem.appendChild(t);
  if(item.class) {
    elem.classList.add(item.class);
  }
  if(item.images.length > 0) {
    item.images.forEach(img_link => {
      img = document.createElement("img");
      img.setAttribute('src', img_link);
      elem.appendChild(img);
    })
  }
  return elem;
}

function setImage(id, image=null) {
  let elem = document.getElementById(id);

  elem.innerHTML = "";
  if(image != null) {
    var img = document.createElement("img");
    img.setAttribute('src', image);
    elem.appendChild(img);
  }
}

chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};

// handle clicks
function gameClickHandler(e) {
  promoteable = document.querySelectorAll('.promote');
  if(promoteable.length > 0) {
    // don't allow additional moves while a piece is waiting to be promoted.
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
    // if this is a destination, call move websocket api
    if(this.classList.contains('destination')) {
      url = document.querySelector('.move_url').dataset.url;
      img_link = otherSelected[0].getElementsByTagName('img')[0].src;
      data = {
        game_id: document.getElementById('game_id').dataset.id,
        destination: {
          row: this.dataset.row,
          column: this.dataset.column,
          id: this.id,
          image: this.getElementsByTagName('img')[0]?.src
        },
        start: {
          row: otherSelected[0].dataset.row,
          column: otherSelected[0].dataset.column,
          id: otherSelected[0].id,
          image: otherSelected[0].getElementsByTagName('img')[0]?.src
        },
      }

      chatSocket.send(JSON.stringify(data));
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
