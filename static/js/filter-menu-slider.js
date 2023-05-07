$('.menu_icon, .close').on('click', function(){
	$('.menu-mobile--itself').toggleClass('show')
})
const menuBlock = document.querySelector('.menu_block');
const menuMobile = document.querySelector('.menu-mobile--itself');
const menuIcon = document.querySelector('.menu_icon');
const body = document.querySelector('body');

menuIcon.addEventListener('click', () => {
  menuMobile.classList.add('show');
  body.style.overflow = 'hidden';
});

menuMobile.addEventListener('click', (event) => {
  if (event.target.classList.contains('close')) {
    menuMobile.classList.remove('show');
    body.style.overflow = '';
    console.log(1)
  }
});