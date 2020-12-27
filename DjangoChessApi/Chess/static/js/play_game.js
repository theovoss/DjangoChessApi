import promote_check from './piece_selection.js';

var squares = document.querySelectorAll(".square");

var game_id =  document.getElementById('game_id').dataset.id;

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
  var elem = document.getElementById('turn');
  elem.innerText = capitalizeFirstLetter(color) + "'s Turn";
}

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

function updateHistory(history_json) {
  console.log("Updating history");
  // update all history
  var elem = document.getElementById("history-content");
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
    setImage(key, value);
  }
  promote_check();
}

function setImage(id, value=null) {
  // <div class="square promote"
  //                 data-row={{row}}
  //                 data-column={{column}}
  //                 data-name={{board|get_item:key|get_item:'name'}}
  //                 data-color={{board|get_item:key|get_item:'color'}}
  // value.name
  // value.color
  let elem = document.getElementById(id);
  var [row, col] = id.split(",");
  var image = value.image;
  if(value.promote_me_daddy) {
    console.log("Promoting at id: " + id);
    elem.classList.add('promote');
    elem.setAttribute('data-row', row);
    elem.setAttribute('data-column', col);
    elem.setAttribute('data-color', value.color);
  } else {
    elem.classList.remove('promote');
  }

  elem.innerHTML = "";
  if(value.image != null) {
    var img = document.createElement("img");
    img.setAttribute('src', image);
    elem.appendChild(img);
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
      var img = document.createElement("img");
      img.setAttribute('src', img_link);
      elem.appendChild(img);
    })
  }
  return elem;
}

chatSocket.onclose = function(e) {
  console.error('Chat socket closed unexpectedly');
};

// handle clicks
function gameClickHandler(e) {
  var promoteable = document.querySelectorAll('.promote');
  if(promoteable.length > 0) {
    // don't allow additional moves while a piece is waiting to be promoted.
    return;
  }
  var otherSelected = document.querySelectorAll('.selected');
  var currentDestinations = document.querySelectorAll('.destination');
  if(otherSelected.length == 0) {
    this.classList.toggle('selected');
    // call to get destinations and select those too.
    var url = document.querySelector('.destinations_url').dataset.url;

    var data = {
      row: this.dataset.row,
      column: this.dataset.column
    }

    const otherParams = getFetchParams(data);

    fetch(url, otherParams)
      .then(response => response.json())
      .then(data => {
        data.forEach(location => {
          var row = location[0];
          var column = location[1];

          var div_id = document.getElementById(row + "," + column);
          div_id.classList.add('destination')
        })
      })
      .catch(error => console.log(error));
  } else {
    // if this is a destination, call move websocket api
    if(this.classList.contains('destination')) {
      var url = document.querySelector('.move_url').dataset.url;
      var img_link = otherSelected[0].getElementsByTagName('img')[0].src;
      var data = {
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
          image: img_link
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
