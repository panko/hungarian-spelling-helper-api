from flask import Blueprint, g, request, render_template, make_response, redirect
from hsha.db import get_db, query_db

bp = Blueprint("login", __name__)


@bp.before_app_request
def load_logged_in_user():
    """If a username is stored in the cokkie, refresh load the user object from
    the database into ``g.user``."""
    username = request.cookies.get('username')

    if username is None:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
        )
        if g.user is None:
            create_user(username)
            g.user = (
                get_db().execute("SELECT * FROM user WHERE username = ?", (username,)).fetchone()
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


def modify_user_score(username, amount):
    user = query_db("select score from user where username=?", [username], True)
    cur = get_db().execute("UPDATE user set score=? where username=?", (amount + user['score'], username))
    res = get_db().commit()
    cur.close()
    return res


def create_user(username):
    get_db().execute("INSERT INTO user (username) values (?)", (username,)).close()
    get_db().commit()
