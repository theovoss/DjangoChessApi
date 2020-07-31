let cards = [...document.querySelectorAll('.card')];

cards.forEach((card) => {
  card.addEventListener('click', expand);
});

function expand(e) {
  cards.forEach((card) => {
    if(this !== card) {
      card.classList.remove('expand');
    }
  })
  this.classList.toggle('expand');
}