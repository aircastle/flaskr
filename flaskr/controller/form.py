from wtforms import (Form,
                     BooleanField,
                     TextField,
                     TextAreaField,
                     PasswordField,
                     HiddenField,
                     SubmitField,
                     validators)

from flaskr.model.user import *
from flaskr.model.entry import *

def check_password():
    def _check_password(form, field):
        user = User.get_from_username_password(
            form.username.data,
            form.password.data)
        if user is None:
            error = 'This login/password combination is not good.'
            raise validators.ValidationError(error)
    return _check_password

def check_entryid():
    def _check_entryid(form, field):
        entry = Entry.get_from_entryid(
            form.entryid.data)
        if entry is None:
            error = 'This Entry ID is invalid.'
            raise validators.ValidationError(error)
    return _check_entryid

class LoginForm(Form):
    username = TextField("Username",
                         validators=[validators.Required(),
                                     validators.Length(min=5, max=30)
                                     ])

    password = PasswordField("Password",
                             validators=[validators.Required(),
                                         validators.Length(min=5, max=30),
                                         check_password()])
    login    = SubmitField("Login")


class AddEntryForm(Form):
    title   = TextField("Title",
                      validators=[validators.Required(),
                                  validators.Length(min=5, max=100)])
    content = TextAreaField("Content",
                            validators=[validators.Required(),
                                        validators.Length(min=5, max=1000)])
    post   = SubmitField("Post")

class AddCommentForm(Form):
    entryid = HiddenField("Entryid",
                        validators=[validators.Required(),
                                    validators.Length(min=5, max=100),
                                    check_entryid()])
    author  = TextField("Author",
                        validators=[validators.Required(),
                                    validators.Length(min=5, max=100)])
    email   = TextField("Email",
                        validators=[validators.Required(),
                                    validators.Email(),
                                    validators.Length(min=5, max=50)])
    url     = TextField("Url",
                        validators=[validators.Required(),
                                    validators.URL(),
                                    validators.Length(min=5, max=50)])
    comment = TextAreaField("Comment",
                            validators=[validators.Required(),
                                        validators.Length(min=5, max=1000)])
    post   = SubmitField("Post")

