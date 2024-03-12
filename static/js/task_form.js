$(function () {
    let form = $('#task_popup')
    let subtask = new SubTasksControl()
    $('.task').on('click', function () {
        if (form.hasClass('opened') && $(this).data("task_id") === form.data("task_id")) {
            closeForm()
        } else {
            form.data("task_id", $(this).data("task_id"))
            return handleTaskForm($(this), false, subtask)
        }
    });
    $('.new_task').on('click', function () {
        if (form.hasClass('opened') && $(this).data("category_id") === form.data("category_id")) {
            closeForm()
        } else {
            form.data("category_id", $(this).data("category_id"))
            return handleTaskForm($(this), true, subtask)
        }
    });
    $('.close').on('click', function () {
        return closeForm()
    });
    form.find("form").submit(function (e) {
        let args = form.data("task_id") ? ("?task_id=" + form.data("task_id")) : ""
        try {
            fetch("/update_subtasks" + args, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify(subtask.getValue.apply(subtask)),

            });
        } catch (e) {
            console.error(e);
        }
    })
});

function SubTasksControl() {
    this.initialize.apply(this)
}

SubTasksControl.prototype.initialize = function (host, component) {
    let thisControl = this
    this.subtasks = {}

    $('#add_subtask').on('click', function () {
        const subtaskName = $('#new_subtask_input').val().trim()
        $('#new_subtask_input').val("")
        if (subtaskName) {
            thisControl.subtasks[subtaskName] = false;
            thisControl.updateList.apply(thisControl)
        }
    });

    thisControl.updateProgress()
}

SubTasksControl.prototype.updateList = function () {
    let thisControl = this
    let index = 1
    $("#sub_task_list_form").empty()
    for (let name in thisControl.subtasks) {
        let newSubtask = $('<div class="form-check subtask">' +
            '<input class="form-check-input subtask_input" form="unlink" type="checkbox" value="" id="subtask' + index + '">' +
            '<label class="form-check-label subtask_name d-inline-block" for="subtask' + index + '"></label>' +
            '<span class="remove_subtask btn d-inline-block">X</span> <hr/></div>')
        newSubtask.find("label").text(name)
        newSubtask.find("input").attr("checked", this.subtasks[name])
        index++;
        $("#sub_task_list_form").append(newSubtask)
    }
    $('.remove_subtask').on('click', function () {
        const subtaskName = $(this).parents('.subtask').find('label').text()
        if (subtaskName) {
            delete thisControl.subtasks[subtaskName]
            thisControl.updateList.apply(thisControl)
        }
    });
    $('.subtask_input').on("change", function () {
        const subtaskName = $(this).parents('.subtask').find('label').text()
        thisControl.subtasks[subtaskName] = this.checked
        thisControl.updateProgress()
    })
    thisControl.updateProgress()
}

SubTasksControl.prototype.updateProgress = function () {
    let done_tasks = Object.values(this.subtasks).filter(e => e == "1").length
    let not_done_tasks = Object.values(this.subtasks).filter(e => e == "0").length
    let progress = done_tasks + not_done_tasks > 0 ? Math.round(done_tasks / (done_tasks + not_done_tasks) * 100) : 0
    $('#task_progress_form').text(progress + "%")
    $('#task_progress_form').attr("style", `width: ${progress}%`)
}

SubTasksControl.prototype.getValue = function () {
    return this.subtasks
}

SubTasksControl.prototype.setValue = function (value) {
    this.subtasks = value
}

function closeForm() {
    let form = $('#task_popup')
    form.slideFadeToggle()
    form.removeClass('opened')
    form.removeData("category_id")
    form.removeData("task_id")
    return false;
}

function handleTaskForm(button, new_form, subtask) {
    let form = $('#task_popup')
    let text_label = $('#task_form_label')
    let html_form = $("#new_task")
    let category_name = button.parents(".category").find(".category-title").text()

    if (!form.hasClass('opened')) {
        form.addClass('opened');
        form.slideFadeToggle();
    }

    subtask.setValue({})

    if (new_form) {
        $("#delete_task").hide()
        html_form.attr("action", `/new_task?category_id=${form.data("category_id")}`)

        html_form.find("#task_form_title").attr("value", "")
        html_form.find("#task_form_description").text("")
        html_form.find("#task_form_expires_on").attr("value", "")

        $("#task_form_submit").attr("value", "Add task")
        text_label.text("Add task to category " + category_name)
        subtask.updateList()
    } else {
        $('#delete_task').attr("action", `/delete_task?task_id=${form.data("task_id")}`)
        $("#delete_task").show()
        html_form.attr("action", `/edit_task?task_id=${form.data("task_id")}`)

        let task_name = button.find(".task__title").text()
        let task_description = button.find(".task__description").text()

        html_form.find("#task_form_title").attr("value", task_name)
        html_form.find("#task_form_description").text(task_description)
        html_form.find("#task_form_expires_on").attr("value", button.data("date_expires"))

        $("#task_form_submit").attr("value", "Edit task")
        text_label.text("Edit task " + task_name + " in category " + category_name)

        try {
            fetch(`/get_subtasks?task_id=${form.data("task_id")}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                },
            }).then(r => r.json()).then(r => {
                subtask.setValue(r)
                subtask.updateList()
            });
        } catch (e) {
            console.error(e);
        }

    }
    return false;
}

$.fn.slideFadeToggle = function (easing, callback) {
    return this.animate({opacity: 'toggle', height: 'toggle'}, 'fast', easing, callback);
};