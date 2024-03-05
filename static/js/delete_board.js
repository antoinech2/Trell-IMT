$(function () {
    let form = $('#warning_popup')
    let text_label = $('#warning-form-label')

    $('.delete_board').on('click', function () {
        if ($(this).data("board_id") === form.data("board_id")) {
            form.removeClass('opened')
            form.slideFadeToggle()
            form.removeData("board_id")
        } else {
            if (!form.hasClass('opened')) {
                form.addClass('opened');
                form.slideFadeToggle();
            }
            form.data("board_id", $(this).data("board_id"))
            let board_name = $("#board_name").text()
            text_label.text("Are you sure to delete the board " + board_name + " ?" )

        }
        return false;
    });

    $('.close_warning_form').on('click', function () {
        form.removeClass('opened')
        form.slideFadeToggle()
        return false;
    });
});

$.fn.slideFadeToggle = function (easing, callback) {
    return this.animate({opacity: 'toggle', height: 'toggle'}, 'fast', easing, callback);
    };
