$(async function () {
    $("#notification_button").on('click', function () {
        try {
            fetch("/get_notifications").then(r => r.json()).then(r => {
                $("#notification_number").text("0")
                $("#read_notifications").empty()
                $("#unread_notifications").empty()
                r.forEach(notif => showNotif(notif))
            });
        } catch (e) {
            console.error(e);
        }

    })
    // Hide notifications when the mouse leaves the notification panel area
    $("#flush-collapseTwo-header").on('mouseleave', function () {
        $(this).collapse('hide');
    });

    $("#notification_number").text(await fetch("/get_notification_count").then(r => r.text()))
})

function showNotif(data) {
    let notificationBadge = $("#notification_number")
    let newNotif = $(`<div class="notification-header"><strong>${data.title}</strong><em class="comment-right" title='${data.time}'>${data.time_message}</em><h6>${data.content}</h6><button class="mark_read"></button></div>`)
    if (data.read){
        newNotif.find(".mark_read").text("Mark as unread")
        $("#read_notifications").append(newNotif)
    }
    else{
        newNotif.find(".mark_read").text("Mark as read")
        $("#unread_notifications").append(newNotif)
        notificationBadge.text(parseInt(notificationBadge.text())+1)
    }
    newNotif.find(".mark_read").on('click', function () {
        try {
            fetch(`/notification_read?notification_id=${data.id}&unread=${data.read}`, {
                method : "PUT"
            }).then(r => r.json()).then(r => {
                newNotif.remove()
                showNotif(r)
                if (!data.read){
                    notificationBadge.text(parseInt(notificationBadge.text())-1)
                }
            })
        } catch (e) {
            console.error(e);
        }
    })
}