$(function () {
    let form = $('#new_task_popup')
    let category_name = $('#add_task_category')
    $('.new_task').on('click', function () {

        if ($(this).data("category_id") === form.data("category_id")) {
            form.removeClass('opened')
            form.slideFadeToggle()
            form.removeData("category_id")
        } else {
            if (!form.hasClass('opened')) {
                form.addClass('opened');
                form.slideFadeToggle();
            }
            form.find("form").attr("action", `/new_task?category_id=${$(this).data("category_id")}`)
            form.data("category_id", $(this).data("category_id"))
            category_name.text($(this).parents(".category").find(".category-title").text())

        }
        return false;
    });

    $('.close').on('click', function () {
        form.removeClass('opened')
        form.slideFadeToggle()
        return false;
    });
});

$.fn.slideFadeToggle = function (easing, callback) {
    return this.animate({opacity: 'toggle', height: 'toggle'}, 'fast', easing, callback);
};