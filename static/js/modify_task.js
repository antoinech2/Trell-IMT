$(function () {
    let form = $('#task_popup')
    let text_label = $('#form-label')
    $('.task').on('click', function () {

        if ($(this).attr("id") === form.data("task_id")) {
            form.removeClass('opened')
            form.slideFadeToggle()
            form.removeData("task_id")
        } else {
            if (!form.hasClass('opened')) {
                form.addClass('opened');
                form.slideFadeToggle();
            }
            form.data("task_id", $(this).attr("id"))
            let html_form = form.find("form")
            html_form.attr("action", `/edit_task?task_id=${$(this).attr("id")}`)
            $('#delete_task').attr("action", `/delete_task?task_id=${$(this).attr("id")}`)

            let task_name = $(this).find(".task__title").text()
            let task_description = $(this).find(".task__description").text()
            let category_name = $(this).parents(".category").find(".category-title").text()
            text_label.text("Edit task " + task_name + " in category " + category_name)
            html_form.find("#title").attr("value", task_name)
            html_form.find("#description").text(task_description)
            $("#form_submit").attr("value", "Edit task")
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