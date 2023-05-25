String.prototype.format = function () {
  var i = 0, args = arguments;
  return this.replace(/{}/g, function () {
    return typeof args[i] != 'undefined' ? args[i++] : '';
  });
};
$('.menu_icon, .close').on('click', function(){
	$('.menu-mobile--itself').toggleClass('show')
})
const menuBlock = document.querySelector('.menu_block');
const menuMobile = document.querySelector('.menu-mobile--itself');
const menuIcon = document.querySelector('.menu_icon');
const closeIcon = document.querySelector('.close');
const body = document.querySelector('body');

menuIcon.addEventListener('click', () => {
  menuMobile.style.top = '{}px'.format(window.pageYOffset.toString() || document.documentElement.toString() || document.body.toString() || 0);
  menuMobile.classList.add('show');
  body.style.overflow = 'hidden';
});

closeIcon.addEventListener('click', (event) => {
  menuMobile.classList.remove('show');
  body.style.overflow = '';
});