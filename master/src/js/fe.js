$(document).ready(function(){
  $('.menu-tab').click(function(){
    $('.menu-tab').removeClass('active');
    $(this).addClass('active');
  });

  $('.dropdown').dropdown();
});



$('select.dropdown').dropdown();


var root = document.documentElement;
const lists = document.querySelectorAll('.hs');

lists.forEach(el => {
  const listItems = el.querySelectorAll('li');
  const n = el.children.length;
  el.style.setProperty('--total', n);
});
