$(function () {
    let form = $('#task_popup')
    $('.task').on('click', function () {
        if ($(this).data("task_id") === form.data("task_id")) {
            closeForm()
        } else {
            form.data("task_id", $(this).data("task_id"))
            return taskForm($(this), false)
        }
    });
    $('.new_task').on('click', function () {
        if ($(this).data("category_id") === form.data("category_id")) {
            closeForm()
        } else {
            form.data("category_id", $(this).data("category_id"))
            return taskForm($(this), true)
        }
    });
    $('.close').on('click', function () {
        return closeForm()
    });
});

function closeForm() {
    let form = $('#task_popup')
    form.slideFadeToggle()
    form.removeClass('opened')
    form.removeData("category_id")
    form.removeData("task_id")
    return false;
}

function taskForm(button, new_form) {
    let form = $('#task_popup')
    let text_label = $('#task_form_label')
    let html_form = form.find("form")
    let category_name = button.parents(".category").find(".category-title").text()

    if (!form.hasClass('opened')) {
        form.addClass('opened');
        form.slideFadeToggle();
    }

    if (new_form) {
        $("#delete_task").hide()
        html_form.attr("action", `/new_task?category_id=${form.data("category_id")}`)

        html_form.find("#task_form_title").attr("value", "")
        html_form.find("#task_form_description").text("")
        html_form.find("#task_form_expires_on").attr("value", "")

        $("#task_form_submit").attr("value", "Add task")
        text_label.text("Add task to category " + category_name)
    } else {
        $('#delete_task').attr("action", `/delete_task?task_id=${button.attr("id")}`)
        $("#delete_task").show()
        html_form.attr("action", `/edit_task?task_id=${form.data("task_id")}`)

        let task_name = button.find(".task__title").text()
        let task_description = button.find(".task__description").text()

        html_form.find("#task_form_title").attr("value", task_name)
        html_form.find("#task_form_description").text(task_description)
        html_form.find("#task_form_expires_on").attr("value", button.data("date_expires"))

        $("#task_form_submit").attr("value", "Edit task")
        text_label.text("Edit task " + task_name + " in category " + category_name)

    }

    return false;
}

$.fn.slideFadeToggle = function (easing, callback) {
    return this.animate({opacity: 'toggle', height: 'toggle'}, 'fast', easing, callback);
};