/**
 * EtiquetteControl is a class for managing etiquettes in a task form.
 */
export function EtiquetteControl() {
    this.initialize();
}

/**
 * Initializes the EtiquetteControl object.
 */
EtiquetteControl.prototype.initialize = function () {
    let thisControl = this;

    // Arrays to store etiquettes of task and list of available etiquettes
    this.etiquetteList = [];
    this.etiquettes = [];

    // Event listener for adding etiquettes
    $('.add_etiquette').on('click', async function () {
        const etiquette_id = $(this).data("etiquette_id");
        // Add selected etiquette
        thisControl.add((await thisControl.getEtiquetteList()).find(etiquette => etiquette.id == etiquette_id));
    });
}

/**
 * Fetches the list of etiquettes asynchronously.
 * @returns {Promise<Array>} - Promise resolving to an array of etiquettes.
 */
EtiquetteControl.prototype.getEtiquetteList = async function () {
    // If etiquette list is not stored locally, fetch it from database
    if (this.etiquetteList.length === 0) {
        try {
            return await fetch(`/get_etiquettes`, {
                method: "GET",
            }).then(r => r.json()).then(r => {
                // Store locally and return result
                this.etiquetteList = r;
                return r;
            });
        } catch (e) {
            console.error(e);
        }
    } else {
        // Return local stored list
        return this.etiquetteList;
    }
}

/**
 * Adds an etiquette to the list.
 * @param {Object} etiquette - Etiquette object to be added.
 */
EtiquetteControl.prototype.add = function ({
                                               id: etiquette_id,
                                               type: etiquette_type,
                                               label: etiquette_name,
                                               color: etiquette_color,
                                               description: etiquette_description
                                           }) {
    let thisControl = this;

    // Have user permission to remove etiquette
    // Developers can't remove etiquette related to priority
    const canRemove = !($("#task_popup").data("user_type") === "Developer" && etiquette_type === "priority");

    // If etiquette is not already added
    if (etiquette_id && !(thisControl.etiquettes.includes(etiquette_id))) {
        // Add to list
        thisControl.etiquettes.push(etiquette_id);

        // Create HTML etiquette badge and display
        let newEtiquette = $(`<span class="badge rounded-pill" data-bs-toggle="tooltip" title="${etiquette_description}" style="background-color:#${etiquette_color !== "None" ? etiquette_color : "000000"}">${etiquette_name}${canRemove ? '<span class="remove-badge remove_etiquette"> X</span>' : ''} </span>`);
        $("#etiquettes_list_form").append(newEtiquette);

        // Create listener attached to etiquette badge to remove etiquette
        newEtiquette.find(".remove_etiquette").on('click', function () {
            // Remove from list and display
            thisControl.etiquettes.splice(thisControl.etiquettes.indexOf(etiquette_id), 1);
            newEtiquette.remove();
        });
    }
}

/**
 * Retrieves the array of etiquettes.
 * @returns {Array} - Array of etiquette IDs.
 */
EtiquetteControl.prototype.getValue = function () {
    return this.etiquettes;
}

/**
 * Resets the EtiquetteControl object by clearing the etiquettes list and UI elements.
 */
EtiquetteControl.prototype.reset = function () {
    // Clear collaborator list and display
    this.etiquettes = [];
    $("#etiquettes_list_form").empty();
}
