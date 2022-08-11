from datetime import datetime
from app import db

class AbstractEntity(db.Model):
    __abstract__ = True
    datetime_created = db.Column(
        db.DateTime,
        default=datetime.now()
    )
    datetime_updated = db.Column(
        db.DateTime,
        default=datetime.now()
    )
    datetime_deleted = db.Column(
        db.DateTime,
        nullable=True
    )