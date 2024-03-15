export function SubTasksControl() {
    this.initialize.apply(this)
}

SubTasksControl.prototype.initialize = function (host, component) {
    let thisControl = this
    this.subtasks = []

    $('#add_subtask').on('click', function () {
        const subtaskName = $('#new_subtask_input').val().trim()
        $('#new_subtask_input').val("")
        if (subtaskName) {
            thisControl.add({name: subtaskName, value: false});
        }
    });

    thisControl.updateProgress()
}

SubTasksControl.prototype.add = function ({name, value}) {
    let thisControl = this

    thisControl.subtasks.push({name, value})
    let newSubtask = $('<div class="form-check subtask">' +
        '<label class="form-check-label subtask_name d-inline-block"><input class="form-check-input subtask_input" form="unlink" type="checkbox" value=""></label>' +
        '<span class="remove_subtask btn d-inline-block">X</span> <hr/></div>')
    newSubtask.find("label").text(name)
    newSubtask.find("input").attr("checked", value)
    $("#sub_task_list_form").append(newSubtask)
    newSubtask.on('click', function () {
        thisControl.subtasks.splice(thisControl.subtasks.indexOf(thisControl.subtasks.find(subtask => subtask.name === name)), 1)
        this.remove()
        thisControl.updateProgress()
    });
    newSubtask.on("change", function () {
        thisControl.subtasks.find(subtask => subtask.name === name).value = this.checked
        thisControl.updateProgress()
    })
    thisControl.updateProgress()
}

SubTasksControl.prototype.updateProgress = function () {
    let done_tasks = this.subtasks.filter(e => e.value == "1").length
    let not_done_tasks = this.subtasks.filter(e => e.value == "0").length
    let progress = done_tasks + not_done_tasks > 0 ? Math.round(done_tasks / (done_tasks + not_done_tasks) * 100) : 0
    $('#task_progress_form').text(progress + "%")
    $('#task_done').text(done_tasks + "/" + (done_tasks + not_done_tasks))
    $('#task_progress_form').attr("style", `width: ${progress}%`)
}

SubTasksControl.prototype.getValue = function () {
    return this.subtasks
}

SubTasksControl.prototype.setValue = function (value) {
    this.subtasks = value
}
