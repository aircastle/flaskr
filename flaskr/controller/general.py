from flask import Module, Flask, request, g, url_for
from flaskr import db, app

@app.before_request
def start_session():
    g.session = db.session

@app.after_request
def close_session(response):
    g.session.close()
    return response

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")
