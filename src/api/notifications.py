from flask import request
from sqlalchemy import desc

from app import app
from flask_login import login_required, current_user

from src.database.database import db
from src.database.models import Notification
from src.helper.date import compare_dates


@app.route('/get_notification_count', methods=['GET'])
@login_required
def get_notification_count():
    """Retrieve notification count of user

    Count all unread notifications of user

    Request response :
    string integer of the number of unread notifications
    """
    return str(Notification.query.filter_by(user_id=current_user.id, read=False).count())


@app.route('/get_notifications', methods=['GET'])
@login_required
def get_notifications():
    """Retrieve all notifications of user

    Return all notifications (read and unread)

    Request response :
    JSON object with list of notifications
    """
    notifs = Notification.query.filter_by(user_id=current_user.id).order_by(desc(Notification.date_created)).all()
    return [parse_notif(notif) for notif in notifs]


@app.route('/notification_read', methods=['PUT'])
@login_required
def set_notification_read():
    """Change the 'readed' state of a notification

    Mark a notification as read or unread

    Request arguments :
    - int : notification_id - The id of the notification to update
    - [boolean : unread] : Mark as unread if true. If not given, mark as read


    Request response :
    JSON object with updated notification
    """
    notif_id = request.args.get('notification_id')
    unread = request.args.get('unread')
    if notif_id:
        notif = Notification.query.filter_by(id=notif_id).first()
        notif.read = not (unread == "true")
        db.session.add(notif)
        db.session.commit()
        return parse_notif(notif)


def parse_notif(notif):
    """Parse notification as JSON dict"""
    return {"time_message": compare_dates(notif.date_created)[1],
            "time": notif.date_created.strftime("%d/%m/%Y %H:%M"),
            **notif.as_dict()}
