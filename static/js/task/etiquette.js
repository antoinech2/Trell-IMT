export function EtiquetteControl() {
    this.initialize.apply(this)
}

EtiquetteControl.prototype.initialize = function (host, component) {
    let thisControl = this
    this.etiquettes = []

    $('.add_etiquette').on('click', function () {
        const etiquette_id = $(this).data("etiquette_id")
        const etiquette_name = $(this).text()
        const etiquette_color = $(this).data("etiquette_color")
        const etiquette_description = $(this).data("etiquette_description")
        thisControl.add({id : etiquette_id, name : etiquette_name, color : etiquette_color, description : etiquette_description})
    });
}

EtiquetteControl.prototype.add = function ({id : etiquette_id, name : etiquette_name, color : etiquette_color, description : etiquette_description}) {
    let thisControl = this

    if (etiquette_id && !(thisControl.etiquettes.includes(etiquette_id))) {
        thisControl.etiquettes.push(etiquette_id);
        let newEtiquette = $(`<span class="badge rounded-pill" data-bs-toggle="tooltip" title="${etiquette_description}" style="background-color:#${etiquette_color !== "None" ? etiquette_color : "000000"}">${etiquette_name}<span\
                class="remove-badge remove_etiquette"> X</span> </span>`)
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
