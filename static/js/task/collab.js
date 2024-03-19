export function CollaboratorControl() {
    this.initialize.apply(this)
}

CollaboratorControl.prototype.initialize = function (host, component) {
    let thisControl = this
    this.userList = []
    this.collaborators = []

    $('#search_user').on('input', async function () {
        let inputValue = $(this).val()
        $("#user_list").empty()
        if (inputValue.length >= 2) {
            let matchUsers = (await thisControl.getUserList()).filter(user => (user.first_name.toLowerCase() + " " + user.last_name.toLowerCase()).includes(inputValue.toLowerCase()))
            for (let user of matchUsers) {
                let newUser = $(`<li class="add_collaborator list-group-item list-group-item-action">${user.first_name} ${user.last_name}</li>`)
                $("#user_list").append(newUser)
                newUser.on('click', function () {
                    thisControl.add(user)
                    $('#search_user').val("")
                    $("#user_list").empty()
                })
            }
        }
    });
}

CollaboratorControl.prototype.getUserList = async function () {
    if (this.userList.length === 0) {
        try {
            return await fetch(`/get_users`, {
                method: "GET",
            }).then(r => r.json()).then(r => {
                this.userList = r
                return r
            });
        } catch (e) {
            console.error(e);
        }
    } else {
        return this.userList
    }
}

CollaboratorControl.prototype.add = async function (user) {
    let thisControl = this

    if (user.id && !(thisControl.collaborators.includes(user.id))) {
        thisControl.collaborators.push(user.id);
        const userTypeManager = ($("#task_popup").data("user_type") !== "Developer")
        let newCollaborator = $(`<span class="collaborator" >${user.first_name} ${user.last_name}${userTypeManager ? '<span\
                class="remove-badge remove_collaborator"> X</span>' : ''} </span>`)
        $("#collaborators").append(newCollaborator)
        newCollaborator.find(".remove_collaborator").on('click', function () {
            thisControl.collaborators.splice(thisControl.collaborators.indexOf(user.id), 1)
            this.remove()
        })
    }
}

CollaboratorControl.prototype.getValue = function () {
    return this.collaborators
}

CollaboratorControl.prototype.reset = function () {
    this.collaborators = []
    $('#search_user').val("")
    $("#collaborators").empty()
}
