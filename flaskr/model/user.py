from werkzeug.security import generate_password_hash, \
    check_password_hash
from hashlib import sha256
from flaskr import db
from flaskr.util.util import *
from sqlalchemy.exc import SQLAlchemyError

class User(db.Model):
    __tablename__   = 'users'
    __mapper_args__ = {}
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name        = db.Column(db.String(length=30), unique=True, nullable = False)
    password    = db.Column(db.String(30), nullable = False)
    email       = db.Column(db.String(50), unique=True, nullable = False)
    delflag     = db.Column(db.Boolean, nullable=False, default = False)
    entries     = db.relationship("Entry", backref="user", cascade='all')

    def __init__(self, name, password, email, delflag=False):
        self.name     = name.lower()
        self.password = sha256(password).hexdigest()
        self.email    = email
        self.delflag  = delflag

    def __repr__(self):
        return "<User('%s', '%s')>" % (self.name, self.password)

    def store_to_db(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            raise SQLAlchemyError

    def delete_from_db(self):
        try:
            self.delflag = True
            # # db.session.
            # db.session.add(self)
            db.session.commit()
        except:
            raise SQLAlchemyError

    def update_to_db(self):
        db.session.commit()

    @classmethod
    def get_from_userid(cls, userid):
        try:
            return cls.query.filter(
                db.and_(cls.id==userid,
                        cls.delflag==False)).one()
        except:
            return None

    @classmethod
    def get_from_username(cls, username):
        try:
            loginname = username.lower()
            return cls.query.filter(
                db.and_(cls.name==username,
                        cls.delflag==False)).one()
        except:
            return None

    @classmethod
    def get_from_username_password(cls, username, password):
        try:
            loginname = username.lower()
            loginpassword = sha256(password).hexdigest()
            return cls.query.filter(db.and_(
                    cls.name==username,
                    cls.password==loginpassword,
                    cls.delflag==False)).first()
        except :
            return None

if __name__=='__main__':
    pass
