from sqlalchemy import func

from src.database.database import db
from src.database.models import Step


def calculate_workload(user):
    return db.session.query(func.count(func.distinct(Step.task_id))) \
        .filter(Step.status == 0, Step.task_id.in_([task.id for task in user.tasks])) \
        .scalar()
