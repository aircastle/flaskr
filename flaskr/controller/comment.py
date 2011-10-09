from flask import (render_template,
                   redirect,
                   url_for,
                   abort,
                   session,
                   escape,
                   request,
                   flash,
                   g)

from flaskr.model.entry import *
from flaskr.model.comment import *
from flaskr.controller.form import *
from flaskr import app

@app.route('/add_comment/', methods=['POST'])
def add_comment():
    form = AddCommentForm(request.form)

    entryid = form.entryid.data
    author  = form.author.data
    comment = form.comment.data
    email   = form.email.data
    url     = form.url.data

    if not form.validate():
        return redirect(url_for('show_entry', entryid=entryid))

    if author.strip() == "" and comment.strip() == "":
        return redirect(url_for('show_entry', entryid=entryid))

    newcomment = Comment(author, comment, email, url)
    entry      = Entry.get_from_entryid(entryid)
    entry.comments.append(newcomment)
    entry.store_to_db()

    flash('New Comment was successfully posted')
    return redirect(url_for('show_entry', entryid=entryid))
