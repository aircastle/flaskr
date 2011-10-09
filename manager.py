from flaskext.script import Manager, Shell
from flaskext.zen import Test, ZenTest
from flaskr import app
from manager.initdb import *
from manager.devserver import *

manager = Manager(app)

def shell_context():
    return dict(app=app)

if __name__=="__main__":
    manager.add_command("initdb", InitDB())
    manager.add_command("dev", DevServer())
    manager.add_command("test", Test())
    manager.add_command("zen", ZenTest())
    manager.add_command("shell", Shell(make_context=shell_context))
    manager.run()

    # config = "flaskr.config.CurrentConfig"
    # app.config.from_object(config)
    # app.run()

