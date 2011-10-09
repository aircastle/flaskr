from flaskr import db

class Base(db.Model):
    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    delflag     = db.Column(db.Boolean, nullable=False, default = False)


    def __init__(self):
        self.delflag  = False

    # def __repr__(self):
    #     return "<User('%s', '%s')>" % (self.name, self.password)

    def store_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        self.delflag = True
        db.session.commit()

    def update_to_db(self):
        db.session.commit()

    @classmethod
    def get_from_id(cls, id, delflag=False):
        try:
            return cls.query.filter(db.and_(
                    cls.id==id,cls.delflag==delflag)).one()
        except:
            return None

if __name__=='__main__':
    pass
