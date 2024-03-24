export function CollaboratorControl(...args) {
    this.initialize(...args)
}

CollaboratorControl.prototype.initialize = function (form_parent, userListParameter = "") {

    let thisControl = this
    this.userList = []
    this.collaborators = []
    this.form_parent = $(form_parent)
    this.getUserListParameter = userListParameter;

    const searchBar = this.form_parent.find('.search_user')
    searchBar.on('input', async function () {
        let inputValue = $(this).val()
        let matchUsers = []
        if (inputValue.length >= 2) {
            matchUsers = (await thisControl.getUserList()).filter(user => (user.first_name.toLowerCase() + " " + user.last_name.toLowerCase()).includes(inputValue.toLowerCase()))
        } else if (thisControl.getUserListParameter) {
            matchUsers = (await thisControl.getUserList())
        }
        thisControl.showUserList(matchUsers)
    });

    searchBar.on('focus', async function () {
        if (thisControl.getUserListParameter) {
            thisControl.showUserList(await thisControl.getUserList())
        }
    })

    /*searchBar.on('blur', async function () {
        thisControl.form_parent.find(".user_list").empty()
    })*/
}

CollaboratorControl.prototype.showUserList = function (matchUsers) {
    let thisControl = this
    thisControl.form_parent.find(".user_list").empty()
    for (let user of matchUsers) {
        let newUser = $(`<li class="add_collaborator list-group-item list-group-item-action">${user.first_name} ${user.last_name} <span class="workload">Working on ${user.workload} tasks</span></li>`)
        thisControl.form_parent.find(".user_list").append(newUser)
        newUser.on('click', function () {
            thisControl.add(user)
            thisControl.form_parent.find('.search_user').val("")
            thisControl.form_parent.find(".user_list").empty()
        })
    }
}

CollaboratorControl.prototype.getUserList = async function () {
    if (this.userList.length === 0) {
        try {
            return await fetch(`/get_users${this.getUserListParameter}`, {
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
        const user_id = $("#user_profile").data("id")
        const canRemove = !(($("#task_popup").data("user_type") === "Developer") || (!this.getUserListParameter && user_id == user.id))
        let newCollaborator = $(`<div ${user_id == user.id ? "style='background-color: #d99216'" : ""} class="collaborator" >${user.first_name} ${user.last_name}${canRemove ? '<span\
                class="remove_collaborator"> <i class="bi bi-x-lg"></i></span>' : ''} </div>`)
        thisControl.form_parent.find(".collaborators").append(newCollaborator)
        newCollaborator.find(".remove_collaborator").on('click', function () {
            thisControl.collaborators.splice(thisControl.collaborators.indexOf(user.id), 1)
            newCollaborator.remove()
        })
    }
}

CollaboratorControl.prototype.getValue = function () {
    return this.collaborators
}

CollaboratorControl.prototype.reset = function () {
    this.collaborators = []
    this.form_parent.find(".user_list").empty()
    this.form_parent.find('.search_user').val("")
    this.form_parent.find(".collaborators").empty()
}
