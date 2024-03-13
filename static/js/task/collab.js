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

CollaboratorControl.prototype.addEtiquette = function (etiquette_id, etiquette_name, etiquette_color, etiquette_description) {
    let thisControl = this

    if (etiquette_id && !(thisControl.collaborators.includes(etiquette_id))) {
        thisControl.collaborators.push(etiquette_id);
        let newEtiquette = $(`<span class="badge rounded-pill" data-bs-toggle="tooltip" title="${etiquette_description}" style="background-color:#${etiquette_color !== "None" ? etiquette_color : "000000"}">${etiquette_name}<span\
                class="remove-badge remove_etiquette"> X</span> </span>`)
        $("#etiquettes_list_form").append(newEtiquette)
        newEtiquette.on('click', function () {
            thisControl.collaborators.splice(thisControl.collaborators.indexOf(etiquette_id), 1)
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
