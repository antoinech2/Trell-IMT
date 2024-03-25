/**
 * SubTasksControl is a class for managing subtasks in a task form.
 */
export function SubTasksControl() {
    this.initialize.apply(this);
}

/**
 * Initializes the SubTasksControl object.
 */
SubTasksControl.prototype.initialize = function () {
    let thisControl = this;

    // Array to store subtasks of task
    this.subtasks = [];

    // Event listener for adding subtasks
    // On click on 'add subtask' button
    $('#add_subtask').on('click', function () {
        const subtaskName = $('#new_subtask_input').val().trim();
        $('#new_subtask_input').val("");
        // Check if name input is filled
        if (subtaskName) {
            thisControl.add({ name: subtaskName, status: false });
        }
    });

    // Initialise progress bar
    thisControl.updateProgress();
}

/**
 * Adds a subtask to the list.
 * @param {Object} subtask - Subtask object to be added.
 */
SubTasksControl.prototype.add = function ({ name, status }) {
    let thisControl = this;

    // Add subtask to list
    thisControl.subtasks.push({ name, status });

    // Create new subtask HTML element and display
    let newSubtask = $(`<div class="form-check subtask"><label class="form-check-label subtask_name d-inline-block"><input class="form-check-input subtask_input" ${status ? "checked" : ""} form="unlink" type="checkbox" value="">${name}</label><span class="remove_subtask btn d-inline-block"><i class="bi bi-x-lg"></i></span> <hr/></div>`);
    $("#sub_task_list_form").append(newSubtask);

    // Create listener attached to remove button of subtask element to remove subtask from list
    newSubtask.find(".remove_subtask").on('click', function () {
        // Remove from list and display
        thisControl.subtasks.splice(thisControl.subtasks.indexOf(thisControl.subtasks.find(subtask => subtask.name === name)), 1);
        newSubtask.remove();

        // Update progress bar
        thisControl.updateProgress();
    });

    // Create listener attached to checkbox of subtask element to toggle 'done' status of subtask
    newSubtask.find("input").on("change", function () {
        // Update internal state of subtask
        thisControl.subtasks.find(subtask => subtask.name === name).status = this.checked;

        // Update progress bar
        thisControl.updateProgress();
    });

    // Update progress bar at subtask creation
    thisControl.updateProgress();
}

/**
 * Updates the progress bar of subtasks.
 */
SubTasksControl.prototype.updateProgress = function () {
    // Calculate number of done and undone subtasks
    let done_tasks = this.subtasks.filter(e => e.status == "1").length;
    let not_done_tasks = this.subtasks.filter(e => e.status == "0").length;
    let progress = done_tasks + not_done_tasks > 0 ? Math.round(done_tasks / (done_tasks + not_done_tasks) * 100) : 0;

    // Update bar text and advancement
    $('#task_progress_form').text(progress + "%");
    $('#task_done').text(done_tasks + "/" + (done_tasks + not_done_tasks));
    $('#task_progress_form').attr("style", `width: ${progress}%`);
}

/**
 * Retrieves the array of subtasks.
 * @returns {Array} - Array of subtasks.
 */
SubTasksControl.prototype.getValue = function () {
    return this.subtasks;
}

/**
 * Resets the SubTasksControl object by clearing the subtasks list and UI elements.
 */
SubTasksControl.prototype.reset = function () {
    // Clear subtask list and display
    this.subtasks = [];
    $("#sub_task_list_form").empty();
    this.updateProgress()
}
