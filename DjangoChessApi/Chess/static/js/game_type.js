buttons = document.querySelectorAll('.game-type-actions button');

buttons.forEach(button => {
  button.onclick = () => {
    if(button.classList.contains('delete')) {
      console.log("calling delete for url" + button.dataset.url);

      // call delete url with fetch
      const otherParams = getFetchParams({}, 'DELETE');

      // TODO: Handle responses somehow. maybe show warning if 400/500
      fetch(button.dataset.url, otherParams)
        .then(response => window.location.href = window.location.href)
        .catch(error => console.log(error));

    } else {
      window.location.href = button.dataset.url;
    }
  }
});
