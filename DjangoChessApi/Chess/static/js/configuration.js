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
  console.log(url);
  group = document.getElementsByName(this.name);
  console.log(group);
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
  console.log(data);

  const otherParams = {
    headers: {
      "content-type": "application/json;",
    },
    body: JSON.stringify(data),
    method: "PATCH"
  }

  fetch(url, otherParams)
    .then(response => console.log(response))
    .catch(error => console.log(error));
}