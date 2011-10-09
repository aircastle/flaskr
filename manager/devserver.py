from flaskext.script import Manager, Server, Shell, Command
from flaskext.debugtoolbar import DebugToolbarExtension
from flaskr import app


class DevServer(Server):
    def handle(self, app, host, port, use_debugger, use_reloader):
        try:
            config = "flaskr.config.DevelopConfig"
            app.config.from_object(config)

            toolbar = DebugToolbarExtension(app)
            # from flaskext.lesscss import lesscss
            # lesscss(app)
        except:pass

        app.run(host=host,
                port=port,
                debug=use_debugger,
                use_reloader=use_reloader,
                **self.server_options)
