let cards = [...document.querySelectorAll('.card')];
let card_images = [...document.querySelectorAll('.card img')];

card_images.forEach((image) => {
  image.addEventListener('click', expand);
});

function expand(e) {
  cards.forEach((card) => {
    if(this.parentElement !== card) {
      card.classList.remove('expand');
    }
  })
  this.parentElement.classList.toggle('expand');
}

var checkboxes = document.querySelectorAll('input[type="checkbox"]');

checkboxes.forEach((checkbox) => checkbox.addEventListener("change", save_checks));

function save_checks(e) {
  url = document.querySelector('.url').dataset.url;
  group = document.getElementsByName(this.name);
  data = {
    index: this.dataset.index,
    piece: this.dataset.piece,
    key: this.dataset.key,
    value: []
  }
  group.forEach((box) => {
    if(box.checked) {
      data.value.push(box.dataset.value);
    }
  });

  const otherParams = {
    headers: {
      "HTTP_X_CSRFTOKEN": getCookie('csrftoken'),
      "content-type": "application/json;",
    },
    body: JSON.stringify(data),
    method: "POST"
  }

  // TODO: Handle responses somehow. Maybe on 400/500 uncheck the box since it didn't save, and maybe show an error...
  fetch(url, otherParams)
    .then(response => console.log(response))
    .catch(error => console.log(error));
}


function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
      const cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
          const cookie = cookies[i].trim();
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) === (name + '=')) {
              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
              break;
          }
      }
  }
  return cookieValue;
}
