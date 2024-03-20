import {CollaboratorControl} from "./task/collab.js";

$(function () {
    let form = $('#board_popup')
    let text_label = $('#board-form-label')
    let collaboratorControl = new CollaboratorControl('#board_popup')

    $('.edit_board').on('click', function () {
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
            let html_form = form.find("form")
            let board_name = $("#board_name").text()
            let board_description = $("#board_description").text()
            text_label.text("Edit board " + board_name)
            html_form.find("#board_form_title").attr("value", board_name)
            html_form.find("#board_form_description").text(board_description)
        }
        return false;
    });

    $('.close_board_form').on('click', function () {
        form.removeClass('opened')
        form.slideFadeToggle()
        return false;
    });

    $("#edit_board").on("submit", function (e) {
        handleFormSubmit(e, collaboratorControl)
    })
});

function handleFormSubmit(e, controller) {
    e.preventDefault()
    let request = e.target.action
    let inputs = e.target.elements
    let body = {
        title: inputs["title"].value,
        description: inputs["description"].value,
        collaborators: controller.getValue()
    }
    try {
        fetch(request, {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        }).then(r => window.location.reload());
    } catch (e) {
        console.error(e);
    }
}

$.fn.slideFadeToggle = function (easing, callback) {
    return this.animate({opacity: 'toggle', height: 'toggle'}, 'fast', easing, callback);
};