$(document).ready(function () {
        var menu = $('.dashboard-menu u');
        menu.click(function () {
            $(this).next().toggleClass('hidden');
        });
});
