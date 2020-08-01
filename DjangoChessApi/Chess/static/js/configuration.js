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