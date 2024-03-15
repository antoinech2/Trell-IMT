from datetime import datetime

from src.database.models import Step, Etiquette


def get_task(task):
    task_dict = task.__dict__

    task_dict['etiquettes'] = [etiquette.__dict__ for etiquette in task.etiquettes]
    task_dict['users'] = [user.__dict__ for user in task.users]

    subtasks_done = Step.query.filter_by(task_id=task_dict["id"], status="1").count()
    subtasks_not_done = Step.query.filter_by(task_id=task_dict["id"], status="0").count()
    if subtasks_done + subtasks_not_done > 0:
        task_dict['progress'] = round(subtasks_done / (subtasks_done + subtasks_not_done) * 100)
    task_dict['subtasks_done'] = subtasks_done
    task_dict['subtasks_total'] = subtasks_done + subtasks_not_done
    if task_dict["date_expires"]:
        expired = False
        delta_date = task_dict["date_expires"] - datetime.now()
        days, seconds = delta_date.days, delta_date.seconds
        if days < 0:
            expired = True
            delta_date = datetime.now() - task_dict["date_expires"]
            days, seconds = delta_date.days, delta_date.seconds
        hours = (days * 24 + seconds) // 3600
        minutes = (abs(seconds) % 3600) // 60
        if abs(days) > 0:
            message_data = "{} days".format(abs(days))
        elif abs(hours) > 0:
            message_data = "{} hours".format(abs(hours))
        else:
            message_data = "{} minutes".format(abs(minutes))
        if expired:
            task_dict["expires_message"] = "Expired {} ago".format(message_data)
            task_dict["has_expired"] = True
        else:
            task_dict["expires_message"] = "Expires in {}".format(message_data)
            task_dict["has_expired"] = False
        task_dict["date_expires"] = task_dict["date_expires"].strftime("%Y-%m-%dT%H:%M")
    return task_dict