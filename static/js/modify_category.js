$(function () {
    let form = $('#category_popup')
    let text_label = $('#category-form-label')
    let board_name = $('#board_name').text()
    $('.edit_category').on('click', function () {
        if ($(this).data("category_id") === form.data("category_id")) {
            form.removeClass('opened')
            form.slideFadeToggle()
            form.removeData("category_id")
        } else {
            if (!form.hasClass('opened')) {
                form.addClass('opened');
                form.slideFadeToggle();
            }
            form.data("category_id", $(this).data("category_id"))
            let html_form = form.find("form")
            html_form.attr("action", `/edit_category?category_id=${$(this).data("category_id")}`)

            let category_name = $(this).parents(".category").find(".category-title").text()
            let category_description = $(this).parents(".category").find(".description-title").text()
            text_label.text("Edit category " + category_name + " in board " + board_name)
            html_form.find("#category_form_title").attr("value", category_name)
            html_form.find("#category_form_description").text(category_description)
            $("#category_form_submit").attr("value", "Edit category")
        }
        return false;
    });

    /*$('.close').on('click', function () {
        form.removeClass('opened')
        form.slideFadeToggle()
        return false;
    });*/
});

$.fn.slideFadeToggle = function (easing, callback) {
    return this.animate({opacity: 'toggle', height: 'toggle'}, 'fast', easing, callback);
};