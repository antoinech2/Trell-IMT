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
                let newUser = $(`<li class="add_collaborator" data-user_id="${user.id}">${user.first_name} ${user.last_name}</li>`)
                $("#user_list").append(newUser)
            }
            $(".add_collaborator").on('click', function() {
                thisControl.addCollaborator($(this).data("user_id"))
            })
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

CollaboratorControl.prototype.add = async function (user_id) {
    let thisControl = this

    if (user_id && !(thisControl.collaborators.includes(user_id))) {
        thisControl.collaborators.push(user_id);
        let user = (await thisControl.getUserList()).find(user => user.id === user_id)
        let newCollaborator = $(`<span class="badge rounded-pill" style="background-color:#000000">${user.first_name} ${user.last_name}<span\
                class="remove-badge remove_collaborator"> X</span> </span>`)
        $("#collaborators").append(newCollaborator)
        newCollaborator.on('click', function () {
            thisControl.collaborators.splice(thisControl.collaborators.indexOf(user_id), 1)
            this.remove()
        })
    }
}

CollaboratorControl.prototype.getValue = function () {
    return this.collaborators
}

CollaboratorControl.prototype.setValue = function (value) {
    this.collaborators = value
}
