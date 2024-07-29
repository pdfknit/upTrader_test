// static/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    var menuItems = document.querySelectorAll('.menu li.has-children > a');

    menuItems.forEach(function(menuItem) {
        menuItem.addEventListener('click', function(event) {
            event.preventDefault();
            var parentLi = menuItem.parentNode;
            var submenu = parentLi.querySelector('ul');
            if (submenu) {
                submenu.style.display = submenu.style.display === 'block' ? 'none' : 'block';
            }
        });
    });
});