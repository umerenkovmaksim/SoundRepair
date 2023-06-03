document.addEventListener("DOMContentLoaded", function() {
  var dropdownItems = document.querySelectorAll(".dropdown-item");

  dropdownItems.forEach(function(item) {
    var submenu = item.querySelector(".right-submenu");

    item.addEventListener("mouseover", function() {
      var objectWidth = submenu.offsetWidth;
      submenu.style.marginRight = -objectWidth * 0.997 + "px";
    });
  });
});
