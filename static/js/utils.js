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
    let newComment = $(`<div class="comment"><strong>${data.title}</strong><em class="comment-right" title='${data.time}'>${data.time_message}</em><h6>${data.content}</h6><div><i class="bi bi-person-fill"></i>${data.author}</div></div>`)
    $("#comments").append(newComment)
}