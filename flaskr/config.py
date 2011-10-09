class Config(object):
    DEBUG                   = False
    TESTING                 = False
    SECRET_KEY              = 'hello world!'
    SESSION_COOKIE_NAME     = "_sid"
#    SQLALCHEMY_DATABASE_URI = 'sqlite:///flaskr/database/flaskr.db'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database/flaskr.db'
    SQLALCHEMY_ECHO         = False

class ProductionConfig(object):
    pass

class DevelopConfig(Config):
    DEBUG           = True
    SQLALCHEMY_ECHO = True
    DEBUG_TB_PANELS = (
        'flaskext.debugtoolbar.panels.headers.HeaderDebugPanel',
        'flaskext.debugtoolbar.panels.logger.LoggingPanel',
        # 'flaskext.debugtoolbar.panels.profiler.ProfilerDebugPanel',
        'flaskext.debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flaskext.debugtoolbar.panels.timer.TimerDebugPanel',
        )
    DEBUG_TB_INTERCEPT_REDIRECTS = False

class TestingConfig(Config):
    TESTING = True

class CurrentConfig(DevelopConfig):
    pass
