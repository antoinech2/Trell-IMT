import {SubTasksControl} from "./subtask.js"
import {EtiquetteControl} from "./etiquette.js"
import {CollaboratorControl} from "./collab.js";


$(function () {
    let form = $('#task_popup')
    let controllers = {subtask : new SubTasksControl(), etiquette : new EtiquetteControl(), collaborator : new CollaboratorControl()}
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
    form.find("form").submit(function(e){
        handleFormSubmit(e, form, controllers)
    })
});

function handleFormSubmit(e, form, controllers) {
    let args = form.data("task_id") ? ("?task_id=" + form.data("task_id")) : ""
    try {
        fetch("/update_subtasks" + args, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(controllers.subtask.getValue()),

        });
    } catch (e) {
        console.error(e);
    }
    try {
        fetch("/update_etiquettes" + args, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(controllers.etiquette.getValue()),

        });
    } catch (e) {
        console.error(e);
    }
    try {
        fetch("/update_collaborators" + args, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(controllers.collaborator.getValue()),

        });
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


    if (new_form) {
        $("#delete_task").hide()
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

function initControllers(task_id, controllers) {
    try {
        fetch(`/get_subtasks?task_id=${task_id}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        }).then(r => r.json()).then(r => {
            for (let task of r) {
                controllers.subtask.add(task)
            }
        });
    } catch (e) {
        console.error(e);
    }

    try {
        fetch(`/get_etiquettes?task_id=${task_id}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        }).then(r => r.json()).then(r => {
            for (let etiquette_task of r) {
                controllers.etiquette.add(etiquette_task.id, etiquette_task.name, etiquette_task.color, etiquette_task.description)
            }
        });
    } catch (e) {
        console.error(e);
    }

    try {
        fetch(`/get_collaborators?task_id=${task_id}`, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        }).then(r => r.json()).then(r => {
            for (let collab of r) {
                controllers.collaborator.add(collab)
            }
        });
    } catch (e) {
        console.error(e);
    }

}

$.fn.slideFadeToggle = function (easing, callback) {
    return this.animate({opacity: 'toggle', height: 'toggle'}, 'fast', easing, callback);
};