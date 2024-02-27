$(function () {
    let form = $('#task_popup')
    let category_name = $('#form-label')
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
            category_name.text("Add to category" + $(this).parents(".category").find(".category-title").text())
            $("#form_submit").text("Edit task")
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