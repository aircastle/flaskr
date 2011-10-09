from flaskr import db
from flaskr.model.entry import *
from flaskr.util.util import *

class Comment(db.Model):
    __tablename__   = 'comments'
    __mapper_args__ = {}
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author      = db.Column(db.String(100), nullable=False)
    comment     = db.Column(db.String(1000), nullable=False)
    email       = db.Column(db.String(50), unique=False, nullable = False)
    url         = db.Column(db.String(50), unique=False, nullable = True)
    date        = db.Column(db.DateTime, unique=True, nullable = False, default = now())
    delflag     = db.Column(db.Boolean, nullable=False, default = False)
    publishflag = db.Column(db.Boolean, nullable=False, default = True)
    entry_id    = db.Column(db.Integer, db.ForeignKey('entries.id'), nullable=False)

    def __init__(self, author, comment, email, url=None, date=None):
        self.author  = author
        self.comment = comment
        self.email = email
        self.url = url
        if date is not None: self.date = date
        # self.date = date

    def __repr__(self):
        return "<Comment('%s', '%s', '%s', '%s')>" % (self.author,
                                                      self.comment,
                                                      self.email,
                                                      self.url)
    def get_entry(self):
        try:
            Entry.query.filter(Entry.id==self.entry_id).one()
        except:
            return None

    # def store_to_db(self):
    #     db.session.add(self)
    #     db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # def update_to_db(self):
    #     db.session.commit()

    @classmethod
    def get_from_commentid(cls, commentid):
        try:
            return cls.query.filter(db.and_(
                    cls.id==commentid,
                    cls.delflag==False,
                    cls.publishflag==True)).one()
        except:
            return None

    @classmethod
    def get_recently(cls, count):
        try:
            comments = cls.query.filter(db.and_(
                    cls.delflag==False,
                    cls.publishflag==True)).order_by('-id').limit(count)
            return comments

        except:
            if count > 1: return []
            else:
                return None

    @classmethod
    def get_from_entryid(cls, entryid):
        try:
            return cls.query.filter(db.and_(
                        cls.entry_id==entryid,
                        cls.delflag==False,
                        cls.publishflag==True)).order_by('id')
        except:
            return None

    @classmethod
    def count_all(cls,):
        return cls.query.count()

if __name__=='__main__':
    pass
