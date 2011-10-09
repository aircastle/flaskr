from flask import Flask, request, g, url_for
from flaskext.sqlalchemy import SQLAlchemy
import config
from flaskr.util.db import db

app = Flask(__name__)

app.config.from_object(config)
app.static_path = '/static'
db.init_app(app)

def url_for_other_page(page):
    args = request.view_args.copy()
    args['page'] = page
    return url_for(request.endpoint, **args)

def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.globals['url_for_other_page'] = url_for_other_page

from flaskr.controller import general, user, entry, comment

# def create_app(config=None):
#     app = Flask(__name__)
#     if config:
#         app.config.from_object(config)
#     else:
#         app.config.from_object(default_settings)

#     app.static_path = '/static'
#     db.init_app(app)

#     app.jinja_env.filters['datetimeformat'] = datetimeformat
#     app.jinja_env.globals['url_for_other_page'] = url_for_other_page
