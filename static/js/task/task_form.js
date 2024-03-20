import {SubTasksControl} from "./subtask.js"
import {EtiquetteControl} from "./etiquette.js"
import {CollaboratorControl} from "./collab.js";


$(function () {
    let form = $('#task_popup')
    let controllers = {
        subtask: new SubTasksControl(),
        etiquette: new EtiquetteControl(),
        collaborator: new CollaboratorControl('#task_popup')
    }
    $('.task').on('click', function () {
        if (form.hasClass('opened') && $(this).data("task_id") === form.data("task_id")) {
            closeForm()
        } else {
            form.data("task_id", $(this).data("task_id"))
            return handleTaskForm($(this), false, controllers)
        }
    });
    $('.new_task').on('click', function () {
        if (form.hasClass('opened') && $(this).data("category_id") === form.data("category_id")) {
            closeForm()
        } else {
            form.data("category_id", $(this).data("category_id"))
            return handleTaskForm($(this), true, controllers)
        }
    });
    $('.close').on('click', function () {
        return closeForm()
    });
    $("#new_task").on("submit", function (e) {
        handleFormSubmit(e, form, controllers)
    })
    $("#comment_form").on("submit", function (e) {
        e.preventDefault();
        const data = new FormData(e.target);
        try {
            fetch(e.target.action, {
                method: "POST",
                body: data,
            }).then(r => r.json()).then(r => {
                showComment(r)
            });
        } catch (e) {
            console.error(e);
        }
        e.target.reset()
    })
});

function handleFormSubmit(e, form, controllers) {
    e.preventDefault()
    let request = e.target.action
    let inputs = e.target.elements
    let body = {
        title: inputs["title"].value,
        description: inputs["description"].value,
        "task-end": inputs["task-end"].value
    }
    Object.entries(controllers).forEach(controller => body[controller[0]] = controller[1].getValue())
    try {
        fetch(request, {
            method: form.data("task_id") ? "PUT" : "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        }).then(r => window.location.reload());
    } catch (e) {
        console.error(e);
    }
}

function closeForm() {
    let form = $('#task_popup')
    form.slideFadeToggle()
    form.removeClass('opened')
    form.removeData("category_id")
    form.removeData("task_id")
    return false;
}

function handleTaskForm(button, new_form, controllers) {
    let form = $('#task_popup')
    let text_label = $('#task_form_label')
    let html_form = $("#new_task")
    let category_name = button.parents(".category").find(".category-title").text()

    if (!form.hasClass('opened')) {
        form.addClass('opened');
        form.slideFadeToggle();
    }

    Object.values(controllers).forEach(controller => controller.reset())
    $("#comments").empty()

    if (new_form) {
        $("#delete_task").hide()
        $("#comment_section").hide()
        html_form.attr("action", `/new_task?category_id=${form.data("category_id")}`)

        html_form.find("#task_form_title").attr("value", "")
        html_form.find("#task_form_description").text("")
        html_form.find("#task_form_expires_on").attr("value", "")

        $("#task_form_submit").attr("value", "Add task")
        text_label.text("Add task to category " + category_name)
    } else {
        $('#delete_task').attr("action", `/delete_task?task_id=${form.data("task_id")}`)
        $("#delete_task").show()
        html_form.attr("action", `/edit_task?task_id=${form.data("task_id")}`)
        $("#comment_form").attr("action", `/new_comment?task_id=${form.data("task_id")}`)
        $("#comment_section").show()

        let task_name = button.find(".task__title").text()
        let task_description = button.find(".task__description").text()

        html_form.find("#task_form_title").attr("value", task_name)
        html_form.find("#task_form_description").text(task_description)
        html_form.find("#task_form_expires_on").attr("value", button.data("date_expires"))

        $("#task_form_submit").attr("value", "Edit task")
        text_label.text("Edit task " + task_name + " in category " + category_name)

        initControllers(form.data("task_id"), controllers)
    }
    return false;
}

function showComment(data) {
    let newComment = $(`<div><p>${data.title}</p><p>${data.content}</p><p>${data.author}</p><p title='${data.time}'>${data.time_message}</p></div>`)
    $("#comments").append(newComment)
}

function initControllers(task_id, controllers) {
    try {
        fetch(`/get_task?task_id=${task_id}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        }).then(r => r.json()).then(r => {
            Object.entries(controllers).forEach(controller => {
                r[controller[0]].forEach(elem => controller[1].add(elem))
            })
            r["comment"].forEach(com => showComment(com))
        });
    } catch (e) {
        console.error(e);
    }

}

$.fn.slideFadeToggle = function (easing, callback) {
    return this.animate({opacity: 'toggle', height: 'toggle'}, 'fast', easing, callback);
};