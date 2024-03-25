/**
 * CollaboratorControl is a class for managing collaborators in a form.
 * @param {string} form_parent - The parent element selector for the form.
 * @param {string} [userListParameter=""] - Additional parameter for fetching user list.
 */
export function CollaboratorControl(...args) {
    this.initialize(...args)
}

/**
 * Initializes the CollaboratorControl object.
 * @param {string} form_parent - The parent element selector for the form.
 * @param {string} [userListParameter=""] - Additional parameter for fetching user list.
 */
CollaboratorControl.prototype.initialize = function (form_parent, userListParameter = "") {
    // Reference to the current object
    let thisControl = this;

    // Array to store the user list and collaborators
    this.userList = [];
    this.collaborators = [];

    // Parent form element
    this.form_parent = $(form_parent);

    // Additional parameter for fetching user list
    // Parameter is defined when searching for new collaborator for a task
    // User list is limited to board's collaborators
    this.getUserListParameter = userListParameter;

    // Event listener for input in the search bar
    const searchBar = this.form_parent.find('.search_user');
    searchBar.on('input', async function () {
        let inputValue = $(this).val();
        let matchUsers = [];
        if (inputValue.length >= 2) {
            // Check for all user match in database
            matchUsers = (await thisControl.getUserList()).filter(user => (user.first_name.toLowerCase() + " " + user.last_name.toLowerCase()).includes(inputValue.toLowerCase()));
        } else if (thisControl.getUserListParameter) {
            // If no input and user filter, show all users
            matchUsers = (await thisControl.getUserList());
        }

        // Display search result
        thisControl.showUserList(matchUsers);
    });

    // Event listener for focusing on the search bar
    searchBar.on('focus', async function () {
        if (thisControl.getUserListParameter) {
            // Show user list when focusing on search bar if user list is filtered (task collaborators)
            thisControl.showUserList(await thisControl.getUserList());
        }
    });
}

/**
 * Displays the list of matched users in the UI.
 * @param {Array} matchUsers - List of matched users.
 */
CollaboratorControl.prototype.showUserList = function (matchUsers) {
    let thisControl = this;
    // Clear previous user list
    thisControl.form_parent.find(".user_list").empty();
    for (let user of matchUsers) {
        // Create new user HTML element and display
        let newUser = $(`<li class="add_collaborator list-group-item list-group-item-action">${user.first_name} ${user.last_name} <span class="workload">Working on ${user.workload} tasks</span></li>`);
        thisControl.form_parent.find(".user_list").append(newUser);

        // Create listener attached to user element to add user to collaborators list
        newUser.on('click', function () {
            thisControl.add(user);
            // Clear search bar
            thisControl.form_parent.find('.search_user').val("");
            thisControl.form_parent.find(".user_list").empty();
        });
    }
}

/**
 * Fetches the user list asynchronously from database.
 * @returns {Promise<Array>} - Promise resolving to an array of user objects.
 */
CollaboratorControl.prototype.getUserList = async function () {
    // If user list is not stored locally, fetch it from database
    if (this.userList.length === 0) {
        try {
            return await fetch(`/get_users${this.getUserListParameter}`, {
                method: "GET",
            }).then(r => r.json()).then(r => {
                // Store locally and return result
                this.userList = r;
                return r;
            });
        } catch (e) {
            console.error(e);
        }
    } else {
        // Return local stored list
        return this.userList;
    }
}

/**
 * Adds a user as a collaborator to task/project.
 * @param {Object} user - User object to be added as a collaborator.
 */
CollaboratorControl.prototype.add = async function (user) {
    let thisControl = this;

    // If user is not already a collaborator
    if (user.id && !(thisControl.collaborators.includes(user.id))) {
        // Add to list
        thisControl.collaborators.push(user.id);
        const user_id = $("#user_profile").data("id");

        // Have user permission to remove collaborator ?
        // Can't remove collaborator if user is Developer
        // Can't remove yourself as collaborator from board
        const canRemove = !(($("#task_popup").data("user_type") === "Developer") || (!this.getUserListParameter && user_id == user.id));

        // Create HTML collaborator badge and display
        let newCollaborator = $(`<div ${user_id == user.id ? "style='background-color: #d99216'" : ""} class="collaborator" >${user.first_name} ${user.last_name}${canRemove ? '<span class="remove_collaborator"> <i class="bi bi-x-lg"></i></span>' : ''} </div>`);
        thisControl.form_parent.find(".collaborators").append(newCollaborator);

        // Create listener attached to collaborator badge to remove collaborator
        newCollaborator.find(".remove_collaborator").on('click', function () {
            // Remove from list and display
            thisControl.collaborators.splice(thisControl.collaborators.indexOf(user.id), 1);
            newCollaborator.remove();
        });
    }
}

/**
 * Retrieves the array of collaborators.
 * @returns {Array} - Array of collaborator IDs.
 */
CollaboratorControl.prototype.getValue = function () {
    return this.collaborators;
}

/**
 * Resets the CollaboratorControl object by clearing collaborators and UI elements.
 */
CollaboratorControl.prototype.reset = function () {
    // Clear collaborator list and display
    this.collaborators = [];
    this.form_parent.find(".user_list").empty();
    this.form_parent.find('.search_user').val("");
    this.form_parent.find(".collaborators").empty();
}
