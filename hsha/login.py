from flask import Blueprint, session, g, request, render_template, make_response, redirect
from hsha import db

bp = Blueprint("login", __name__)


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for("login.index"))

        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    """If a username is stored in the cokkie, refresh load the user object from
    the database into ``g.user``."""
    username = request.cookies.get('username')

    if username is None:
        g.user = None
    else:
        g.user = (
            db.get_db().execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        )
        if g.user is None:
            db.create_user(username)
            g.user = (
                db.get_db().execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
            )

@bp.route('/')
def index():
    username = request.cookies.get('username')
    return render_template('index.html', username=username)


@bp.route('/login', methods=['POST', 'GET'])
def setusernamecookie():
    if request.method == 'POST':
        user = request.form['username']
        resp = make_response(redirect("/"))
        resp.set_cookie('username', user)
        load_logged_in_user()
        return resp

    if request.method == 'GET':
        return redirect("/")


@bp.route('/logout', methods=['POST', 'GET'])
def logout():
    resp = make_response(redirect('/'))
    resp.set_cookie('username', '', expires=0)
    return resp
