
function historyClickHandler(e) {
  url = this.dataset.url;

  const otherParams = getFetchParams({});

  fetch(url, otherParams)
    .then(_ => location.reload())
    .catch(error => console.log(error));
};

history_links = document.querySelectorAll(".history_action");

history_links.forEach(link => {
  link.addEventListener('click', historyClickHandler);
});

let history = document.querySelector('.history-content');
history.scrollTop = 99999999;