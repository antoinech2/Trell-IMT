from src.database.models import Step
from src.helper.date import compare_dates


def get_task(task):
    """Calculate task additional information for display

    :param Task task: task to be displayed

    :return dict: Task full information

    """
    # Get database information
    task_dict = task.__dict__

    # Get etiquettes and collaborators informations
    task_dict['etiquettes'] = [etiquette.as_dict() for etiquette in task.etiquettes]
    task_dict['users'] = [user.__dict__ for user in task.users]

    # Calculate number of done and undone subtasks
    # Calculate the progress of task in percentage
    subtasks_done = Step.query.filter_by(task_id=task_dict["id"], status="1").count()
    subtasks_not_done = Step.query.filter_by(task_id=task_dict["id"], status="0").count()
    if subtasks_done + subtasks_not_done > 0:
        task_dict['progress'] = round(subtasks_done / (subtasks_done + subtasks_not_done) * 100)
    task_dict['subtasks_done'] = subtasks_done
    task_dict['subtasks_total'] = subtasks_done + subtasks_not_done

    # If date has expiration, calculate string to display
    if task_dict["date_expires"]:
        expired, message_data = compare_dates(task_dict["date_expires"])
        task_dict["has_expired"] = expired
        task_dict["expires_message"] = "Expired " if expired else "Expires "
        task_dict["expires_message"] += message_data
        task_dict["date_expires"] = task_dict["date_expires"].strftime("%Y-%m-%dT%H:%M")

    # Return dict with complete information
    return task_dict
