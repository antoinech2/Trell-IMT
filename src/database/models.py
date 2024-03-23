import enum
from datetime import datetime

from src.database.database import db


class UserType(enum.Enum):
    ProjectManager = 1
    Developer = 2


class Language(enum.Enum):
    French = 1
    English = 2


class TaskRelation(enum.Enum):
    Manager = 1
    Reviewer = 2
    Assignee = 3


BoardUsers = db.Table('BoardUsers',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
                      db.Column('board_id', db.Integer, db.ForeignKey('board.id'), nullable=False),
                      db.PrimaryKeyConstraint('user_id', 'board_id'))

EtiquetteTask = db.Table('EtiquetteTask',
                         db.Column('task_id', db.Integer, db.ForeignKey('task.id'), nullable=False),
                         db.Column('etiquette_id', db.Integer, db.ForeignKey('etiquette.id'), nullable=False),
                         db.PrimaryKeyConstraint('task_id', 'etiquette_id'))

UserTask = db.Table('UserTask',
                    db.Column('task_id', db.Integer, db.ForeignKey('task.id'), nullable=False),
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), nullable=False),
                    db.PrimaryKeyConstraint('task_id', 'user_id'))


class User(db.Model):
    __tablename__: str = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.Enum(UserType), nullable=False)
    password = db.Column(db.String(), nullable=False)
    authenticated = db.Column(db.Boolean, default=False)
    language = db.Column(db.Enum(Language))
    boards = db.relationship('Board', secondary=BoardUsers, backref='users')
    tasks = db.relationship('Task', secondary=UserTask, backref='users')

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False


class Board(db.Model):
    __tablename__: str = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())


class Category(db.Model):
    __tablename__: str = 'category'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())


class Task(db.Model):
    __tablename__: str = 'task'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    date_expires = db.Column(db.DateTime, nullable=True)
    etiquettes = db.relationship('Etiquette', backref='tasks', secondary=EtiquetteTask)


class Etiquette(db.Model):
    __tablename__: str = 'etiquette'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(), nullable=False)
    label = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    color = db.Column(db.String(), nullable=True)


class Step(db.Model):
    __tablename__: str = 'step'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    status = db.Column(db.Boolean, nullable=False, default=False)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())


class Commentary(db.Model):
    __tablename__: str = 'commentary'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.String())
    date_created = db.Column(db.DateTime)


class Notification(db.Model):
    __tablename__: str = 'notification'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    read = db.Column(db.Boolean, default=False, nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
