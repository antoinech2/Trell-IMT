$(function () {
    let form = $('#new_category_popup')
    let board_name = $('#add_category_board')
    $('.new_category').on('click', function () {

        if (form.hasClass('opened')) {
            form.removeClass('opened')
            form.slideFadeToggle()
        } else {
            form.addClass('opened');
            form.slideFadeToggle();
            board_name.text($("#board_name").text())

        }
        return false;
    });

    $('.close_category_form').on('click', function () {
        form.removeClass('opened')
        form.slideFadeToggle()
        return false;
    });
});

$.fn.slideFadeToggle = function (easing, callback) {
    return this.animate({opacity: 'toggle', height: 'toggle'}, 'fast', easing, callback);
};