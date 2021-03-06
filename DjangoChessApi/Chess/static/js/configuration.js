let cards = [...document.querySelectorAll('.card')];
let card_images = [...document.querySelectorAll('.card img')];
let delete_button = document.querySelector('.delete')

delete_button.onclick = () => {
  const otherParams = getFetchParams({}, 'DELETE');

  // TODO: Handle responses somehow. maybe show warning if 400/500
  fetch(delete_button.dataset.url, otherParams)
    .then(_ => window.location.href = delete_button.dataset.redirect_url)
    .catch(error => console.log(error));
}

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

checkboxes.forEach((checkbox) => {
  if(checkbox.classList.contains("not_this_one")) {
    return;
  }
  checkbox.addEventListener("change", save_checks);
});

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

  const otherParams = getFetchParams(data);

  // TODO: Handle responses somehow. Maybe on 400/500 uncheck the box since it didn't save, and maybe show an error...
  fetch(url, otherParams)
    .then(response => console.log(response))
    .catch(error => console.log(error));
}

function json_beautify(id) {
  var elem = document.getElementById(id);

  var obj = JSON.parse( elem.value.replace(/'/g, '"') );
  var pretty = JSON.stringify(obj, undefined, 4);
  elem.value = pretty;
};

// Then use it like this on any textarea
json_beautify("raw");

function toggle_raw() {
  document.getElementById("raw").classList.toggle("d-none");
  document.getElementById("formatted").classList.toggle("d-none");
}