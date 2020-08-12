import sqlite3

import click
import json
from flask import current_app
from flask import g
from flask.cli import with_appcontext


def get_db():
    """Connect to the application's configured database. The connection
    is unique for each request and will be reused if this is called
    again.
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables."""
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

def format_word(word):
    res = word.split(" ")[0]
    res = res.lower()
    return res


def init_words_into_db():
    """Read in the words and create the data."""
    db = get_db()

    with open("tools/words.json") as jsonfile:
        data = json.load(jsonfile)
        try:
            for word in data['j']:
                word = format_word(word)
                db.execute("INSERT INTO word (word, is_j) VALUES ('{}',true)".format(word))
            for word in data['ly']:
                word = format_word(word)
                db.execute("INSERT INTO word (word, is_j) VALUES ('{}',false)".format(word))
        except sqlite3.IntegrityError:
            print("the word '{}' is already in the database. has both characters.".format(word))
        db.commit()


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear existing data and create new tables."""
    init_db()
    init_words_into_db()
    click.echo("Initialized the database.")


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
