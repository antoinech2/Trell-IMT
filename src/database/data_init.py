from src.database.database import db
from src.database.models import Etiquette


def insert_initial_values(*args, **kwargs):
    db.session.add(Etiquette(type="priority", label="Critical", description="Most important task"))
    db.session.add(Etiquette(type="priority", label="High", description="Import task"))
    db.session.add(Etiquette(type="priority", label="Medium", description="Quite important task"))
    db.session.add(Etiquette(type="priority", label="Low", description="Not important task"))
    db.session.add(Etiquette(type="priority", label="Lowest", description="Lowest important task"))
    db.session.add(Etiquette(type="status", label="Not started", description="Planned but not started yet"))
    db.session.add(Etiquette(type="status", label="In progress", description="Work in progress"))
    db.session.add(Etiquette(type="status", label="Blocked", description="Blocked by other task"))
    db.session.add(Etiquette(type="status", label="Abandoned", description="Will not be pursued"))
    db.session.add(Etiquette(type="status", label="Finished", description="Task done"))
    db.session.add(Etiquette(type="status", label="Waiting", description="Waiting for more information"))
    db.session.add(Etiquette(type="status", label="In study", description="Task not planned yet"))
    db.session.add(Etiquette(type="status", label="Stand-by", description="Paused task"))
    db.session.commit()
