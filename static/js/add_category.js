$(function () {
    let form = $('#category_popup')
    let text_label = $('#category-form-label')
    let board_name = $('#board_name').text()
    let board_id = $('#board').data("id")
    $('.new_category').on('click', function () {

        if (form.hasClass('opened')) {
            form.removeClass('opened')
            form.slideFadeToggle()
        } else {
            let html_form = form.find("form")
            html_form.attr("action", `/new_category?board_id=${board_id}`)
            form.addClass('opened');
            form.slideFadeToggle();
            $("#category-form-label").text($("#board_name").text())
            text_label.text("Add new category in board " + board_name)
            html_form.find("#category_form_title").attr("value", "")
            html_form.find("#category_form_description").text("")
            $("#category_form_submit").attr("value", "Add category")
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