import enum

from database import db


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
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                      db.Column('board_id', db.Integer, db.ForeignKey('board.id')))

EtiquetteTask = db.Table('EtiquetteTask',
                         db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
                         db.Column('etiquette_id', db.Integer, db.ForeignKey('etiquette.id')))

UserTask = db.Table('UserTask',
                    db.Column('task_id', db.Integer, db.ForeignKey('task.id')),
                    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                    db.Column('association_type', db.Enum(TaskRelation)))


class User(db.Model):
    __tablename__: str = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    type = db.Column(db.Enum(UserType), nullable=False)
    password = db.Column(db.String(), nullable=False)
    language = db.Column(db.Enum(Language))
    boards = db.relationship('Board', secondary=BoardUsers, backref='boards')
    tasks = db.relationship('Task', secondary=UserTask, backref='tasks')


class Board(db.Model):
    __tablename__: str = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    users = db.relationship('User', secondary=BoardUsers, backref='users')


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
    priority = db.Column(db.Integer, nullable=True)
    etiquettes = db.relationship('Etiquette', backref='etiquettes', secondary=EtiquetteTask)
    users = db.relationship('User', secondary=UserTask, backref='users')


class Etiquette(db.Model):
    __tablename__: str = 'etiquette'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    label = db.Column(db.String(), nullable=True)
    description = db.Column(db.String())
    tasks = db.relationship('Task', backref='tasks', secondary=EtiquetteTask)


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
