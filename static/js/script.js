var tree = document.getElementById('tree');

for(let ul of tree.querySelectorAll('ul')){
    ul.hidden = true;
}


tree.onclick = function (event) {
    if (event.target.tagName != 'SPAN') return;

    let childrenContainer = event.target.parentNode.querySelector('ul');

    if (!childrenContainer) return;

    childrenContainer.hidden = !childrenContainer.hidden;

    if(childrenContainer.hidden) {
        event.target.classList.add('hide');
        event.target.classList.remove('show');
	event.target.classList.remove('open');
        event.target.classList.remove('active');
    } else {
        event.target.classList.toggle('active');
	event.target.classList.toggle("open");
        event.target.classList.add('show');
        event.target.classList.remove('hide');
    }
};

// const openMenu = document.querySelector('.open-menu'),
//     menuPanel = document.querySelector('.menu'),
//menuClosed = document.querySelector('.menu-header__burger');

//menuClosed.addEventListener('click', () => {
//    menuPanel.classList.add('visible');
//})

//openMenu.addEventListener('click', () => {
//    menuPanel.classList.remove('visible');
//})

const login = document.querySelector('.header-wrapper__login'),
      overlay = document.querySelector('.overlay'),
      close = document.querySelector('.form-close');

login.addEventListener('click', () => {
      overlay.classList.add('overlayOn');
})

close.addEventListener('click', () => {
      overlay.classList.remove('overlayOn');
})


//const searchtest = document.querySelector('.menu-search__field'),
//      searchField = document.querySelector('.modal-search'),
//      searchClose = document.querySelector('.modal-search__back');


//searchtest.addEventListener('click', () => {
//   searchField.classList.add('show');

//})

//searchClose.addEventListener('click', () => {
//    searchField.classList.remove('show');
//})






