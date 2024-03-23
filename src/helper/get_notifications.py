from app import app
from flask_login import login_required, current_user

from src.database.models import Notification
from src.helper.date import compare_dates


@app.route('/get_notifications', methods=['GET'])
@login_required
def get_notifications():
    notifs = Notification.query.filter_by(user_id=current_user.id).all()
    return [{"time_message": compare_dates(notif.__dict__["date_created"])[1],
             "time": notif.__dict__["date_created"].strftime("%d/%m/%Y %H:%M"),
             **{arg: notif.__dict__[arg] for arg in ["title", "content", "read"]}}
            for notif in notifs]
