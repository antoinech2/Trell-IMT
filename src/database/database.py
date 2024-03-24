from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_database():
    """Create database at initialization"""
    db.create_all()
