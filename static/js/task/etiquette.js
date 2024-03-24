export function EtiquetteControl() {
    this.initialize.apply(this)
}

EtiquetteControl.prototype.initialize = function () {
    let thisControl = this
    this.etiquetteList = []
    this.etiquettes = []

    $('.add_etiquette').on('click', async function () {
        const etiquette_id = $(this).data("etiquette_id")
        thisControl.add((await thisControl.getEtiquetteList()).find(etiquette => etiquette.id == etiquette_id))
    });
}

EtiquetteControl.prototype.getEtiquetteList = async function () {
    if (this.etiquetteList.length === 0) {
        try {
            return await fetch(`/get_etiquettes`, {
                method: "GET",
            }).then(r => r.json()).then(r => {
                this.etiquetteList = r
                return r
            });
        } catch (e) {
            console.error(e);
        }
    } else {
        return this.etiquetteList
    }
}

EtiquetteControl.prototype.add = function ({id : etiquette_id, type : etiquette_type, label : etiquette_name, color : etiquette_color, description : etiquette_description}) {
    let thisControl = this
    const canRemove = !($("#task_popup").data("user_type") === "Developer" && etiquette_type === "priority")

    if (etiquette_id && !(thisControl.etiquettes.includes(etiquette_id))) {
        thisControl.etiquettes.push(etiquette_id);
        let newEtiquette = $(`<span class="badge rounded-pill" data-bs-toggle="tooltip" title="${etiquette_description}" style="background-color:#${etiquette_color !== "None" ? etiquette_color : "000000"}">${etiquette_name}${canRemove ? '<span\
                class="remove-badge remove_etiquette"> X</span>' : ''} </span>`)
        $("#etiquettes_list_form").append(newEtiquette)
        newEtiquette.find(".remove_etiquette").on('click', function () {
            thisControl.etiquettes.splice(thisControl.etiquettes.indexOf(etiquette_id), 1)
            newEtiquette.remove()
        })
    }
}

EtiquetteControl.prototype.getValue = function () {
    return this.etiquettes
}

EtiquetteControl.prototype.reset = function () {
    this.etiquettes = []
    $("#etiquettes_list_form").empty()
}
