export function initControllers(request, controllers) {
    try {
        fetch(request, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            },
        }).then(r => r.json()).then(r => {
            Object.entries(controllers).forEach(controller => {
                r[controller[0]].forEach(elem => controller[1].add(elem))
            })
            r["comment"]?.forEach(com => showComment(com))
        });
    } catch (e) {
        console.error(e);
    }
}

export function showComment(data) {
    let newComment = $(`<div><p>${data.title}</p><p>${data.content}</p><p>${data.author}</p><p title='${data.time}'>${data.time_message}</p></div>`)
    $("#comments").append(newComment)
}