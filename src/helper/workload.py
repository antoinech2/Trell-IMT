from sqlalchemy import func

from src.database.database import db
from src.database.models import Step


def calculate_workload(user):
    """Calculate workload of user

    Workload is number of unfinished task in which user is assigned

    :param User user: User whose workload is to be calculated

    :return int: Workload of user

    """
    # Query tasks where there is an undone subtask
    return db.session.query(func.count(func.distinct(Step.task_id))) \
        .filter(Step.status == 0, Step.task_id.in_([task.id for task in user.tasks])) \
        .scalar()
