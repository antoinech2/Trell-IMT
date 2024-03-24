from src.database.models import Step
from src.helper.date import compare_dates


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
        expired, message_data = compare_dates(task_dict["date_expires"])
        task_dict["has_expired"] = expired
        task_dict["expires_message"] = "Expired " if expired else "Expires "
        task_dict["expires_message"] += message_data
        task_dict["date_expires"] = task_dict["date_expires"].strftime("%Y-%m-%dT%H:%M")
    return task_dict
