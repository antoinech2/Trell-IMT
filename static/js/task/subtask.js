
export function SubTasksControl() {
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
    $('#task_done').text(done_tasks+"/"+(done_tasks+not_done_tasks))
    $('#task_progress_form').attr("style", `width: ${progress}%`)
}

SubTasksControl.prototype.getValue = function () {
    return this.subtasks
}

SubTasksControl.prototype.setValue = function (value) {
    this.subtasks = value
}
