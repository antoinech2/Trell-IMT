$(async function () {
    $("#notification_button").on('click', function () {
        try {
            fetch("/get_notifications").then(r => r.json()).then(r => {
                $("#notifications").empty()
                r.forEach(notif => showNotif(notif))
            });
        } catch (e) {
            console.error(e);
        }

    })

    $("#notification_number").text(await fetch("/get_notification_count").then(r => r.text()))
})

function showNotif(data) {
    let newNotif = $(`<div class="notification"><strong>${data.title}</strong><em class="comment-right" title='${data.time}'>${data.time_message}</em><h6>${data.content}</h6></div>`)
    $("#notifications").append(newNotif)
}