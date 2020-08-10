buttons = document.querySelectorAll('.game-type-actions button');

buttons.forEach(button => {
  button.onclick = () => {
    window.location.href = button.dataset.url;
  }
});
