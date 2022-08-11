from datetime import datetime, timedelta
import enum
from operator import and_
from marshmallow import validates
from werkzeug.security import (
    generate_password_hash, 
    check_password_hash,
)

from app import db
import utils



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


    @classmethod
    def get_all_existing(cls):
        return cls.query.filter_by(datetime_deleted=None)


    @classmethod
    def get_all(cls):
        return cls.query.all()


    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(and_(cls.datetime_deleted==None, cls.id==id)).first()


    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            print(f"We have a problem: {e}")


    def delete(self):
        self.datetime_deleted = datetime.now()


class User(AbstractEntity):
    id = db.Column(db.Integer, primary_key=True)
    iin = db.Column(db.String(12), unique=True)
    name = db.Column(db.String(250))
    email = db.Column(db.String(60))
    password_hash = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise AttributeError("password is not readable attribute!")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @validates("email")
    def validate_email(self, key, address):
        if '@' not in address:
            raise ValueError("failed simple email validation")
        return address

    @validates("iin")
    def validate_iin(self, key, value):
        users: list = User.get_all()
        for user in users:
            if user.iin == value:
                raise ValueError("iin is already exist")

        return value


    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


class Card(AbstractEntity):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    number = db.Column(db.String(16), unique=True)
    validity_period = db.Column(db.Date, default=(datetime.now()+timedelta(365*3)))
    cvv = db.Column(db.String(3), default=utils.generate_cvv())
    is_active = db.Column(db.Boolean, default=True)
    balance = db.Column(db.Float, default=0)

    @classmethod
    def get_by_owner(cls, id):
        return cls.query.filter_by(owner_id=id).first()
    
    
    @classmethod
    def get_active_by_owner(cls, id):
        """Found card by owner id. The card must be active"""
        return cls.query.filter(and_(cls.owner_id==id, cls.is_active==True)).first()

    
    @classmethod
    def get_all_active(cls):
        """Found active card. Return queryset"""
        return cls.query.filter_by(is_active=True)
    
    
    @classmethod
    def get_active_by_id(cls, id):
        """Found number by id and active"""
        return cls.query.filter(and_(cls.is_active==True, cls.id==id)).first()
    
    
    @classmethod
    def get_by_number(cls, num):
        """Found number by number and not deleted"""
        return cls.query.filter(
            and_(
                cls.datetime_deleted==None, 
                cls.number==num
            )
        ).first()


class Status(enum.Enum):
    ok = "Successful"
    bad = "Rejected"
    time = "Late"


class Transaction(AbstractEntity):
    id = db.Column(db.Integer, primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'))
    status = db.Column(db.Enum(Status))
    


