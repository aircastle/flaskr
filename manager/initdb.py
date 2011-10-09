from flask import g
from flaskext.script import Command
from flaskext.sqlalchemy import SQLAlchemy
from flaskr import app, db
from flaskr.model.user import *
from flaskr.model.entry import *
from flaskr.model.comment import *

config = "flaskr.config.Config"
app.config.from_object(config)

class InitDB(Command):
    def __init__(self):
        pass

    # def get_options(self):
    #     pass

    def run(self):
        db.metadata.drop_all(bind=db.engine)
        db.metadata.create_all(bind=db.engine)

        g.session = db.session
        admin = User("admin", "admin123", "admin@example.com")
        g.session.add(admin)
        g.session.commit()

        g.session.close()
