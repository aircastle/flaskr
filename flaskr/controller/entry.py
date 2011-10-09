from flask import (render_template,
                   redirect,
                   url_for,
                   abort,
                   session,
                   escape,
                   request,
                   flash,
                   g)

from flaskext.login import *

from flaskr.util.util import *
from flaskr.model.entry import *
from flaskr.model.user import *
from flaskr.model.comment import *
from flaskr.controller.form import *
from flaskr import app

@app.route('/', defaults={'page':1})
@app.route('/page/<int:page>')
def show_entries(page):
    form     = AddEntryForm(request.form)
    PER_PAGE = 5
    count    = Entry.count_all()
    entries  = Entry.get_for_page(page, PER_PAGE)

    if not entries and page != 1: abort(404)
    pagination = Pagination(page, PER_PAGE, count)

    rentries = Entry.get_recently(10)
    rcomments = Comment.get_recently(10)

    return render_template('top.html',
                           entries=entries,
                           pagination=pagination,
                           recententries=rentries,
                           recentcomments=rcomments,
                           form=form)

@app.route('/entry/<int:entryid>')
def show_entry(entryid):
    form = AddCommentForm(request.form)
    entry  = Entry.get_from_entryid(entryid)
    comments = entry.comments
    if not entry: abort(404)
    return render_template('show_entry.html',
                           entry=entry,
                           comments=comments,
                           form=form)

@app.route('/add_entry', methods=['POST'])
@login_required
def add_entry():
    form = AddEntryForm(request.form)
    if not form.validate(): return redirect(url_for('show_entries'))

    title   = form.title.data
    content = form.content.data
    if title.strip() == "" and content.strip() == "":
        return redirect(url_for('show_entries'))

    newentry = Entry(title, content)
    user = User.get_from_userid(current_user.id)
    user.entries.append(newentry)
    user.store_to_db()

    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))
