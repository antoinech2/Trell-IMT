from src.database.database import db
from src.database.models import Etiquette


def insert_initial_values(*args, **kwargs):
    db.session.add(Etiquette(type="priority", label="Critical", description="Most important task", color="f50a0a"))
    db.session.add(Etiquette(type="priority", label="High", description="Import task", color="f5830a"))
    db.session.add(Etiquette(type="priority", label="Medium", description="Quite important task", color="f5e10a"))
    db.session.add(Etiquette(type="priority", label="Low", description="Not important task", color="1af045"))
    db.session.add(Etiquette(type="priority", label="Lowest", description="Lowest important task", color="2ef2df"))
    db.session.add(Etiquette(type="status", label="Not started", description="Planned but not started yet", color="6d6f8a"))
    db.session.add(Etiquette(type="status", label="In progress", description="Work in progress", color="424bc2"))
    db.session.add(Etiquette(type="status", label="Blocked", description="Blocked by other task", color="6e4343"))
    db.session.add(Etiquette(type="status", label="Abandoned", description="Will not be pursued", color="5f0c78"))
    db.session.add(Etiquette(type="status", label="Finished", description="Task done", color="00a613"))
    db.session.add(Etiquette(type="status", label="Waiting", description="Waiting for more information", color="d106ce"))
    db.session.add(Etiquette(type="status", label="In study", description="Task not planned yet", color="8c6d08"))
    db.session.add(Etiquette(type="status", label="Stand-by", description="Paused task", color="757171"))
    db.session.commit()
