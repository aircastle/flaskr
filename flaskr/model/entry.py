from flaskr import db
from flaskr.util.util import *

class Entry(db.Model):
    __tablename__   = 'entries'
    __mapper_args__ = {}
    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title     = db.Column(db.String(100), nullable=False)
    content   = db.Column(db.String(1000), nullable=False)
    date      = db.Column(db.DateTime, nullable=False, default=now())
    delflag   = db.Column(db.Boolean, nullable=False, default = False)
    draftflag = db.Column(db.Boolean, nullable=False, default = False)
    user_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    comments  = db.relationship("Comment", backref="entry", cascade='all')

    def __init__(self, title, content, date=None):
        self.title   = title
        self.content = content
        if date is not None:
            self.date = date

    def __repr__(self):
        return "<Entry('%s', '%s')>" % (self.title, self.content)

    def store_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # def update_to_db(self):
    #     db.session.commit()

    def count_comment(self):
        try:
            return len(self.comments)
        except:
            return 0

    @classmethod
    def get_from_entryid(cls, entryid):
        try:
            return cls.query.filter(db.and_(
                    cls.id==entryid,
                    cls.delflag==False,
                    cls.draftflag==False)).one()
        except:
            return None

    @classmethod
    def get_recently(cls, count):
        try:
            return cls.query.filter(db.and_(
                    cls.delflag==False,
                    cls.draftflag==False)).order_by('-id').limit(count)
        except:
            if count > 1:return []
            else:return None

    @classmethod
    def get_for_page(cls, page, PER_PAGE):
        try:
            count = cls.count_all()
            offset = PER_PAGE * (page - 1)
            return cls.query.filter(db.and_(
                        cls.delflag==False,
                        cls.draftflag==False)).\
                                        order_by('-id').limit(PER_PAGE).offset(offset)
        except:
            if PER_PAGE > 1:return []
            else:return None

    @classmethod
    def count_all(cls,):
        try:
            return cls.query.filter(cls.delflag==False).count()
        except:
            return None


if __name__=='__main__':
    pass
