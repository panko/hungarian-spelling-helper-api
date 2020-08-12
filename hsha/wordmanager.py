from flask import Blueprint, session, g, request, render_template, make_response, redirect, jsonify, current_app, flash
import sqlite3
from hsha import db
from hsha import game

bp = Blueprint("wordmanager", __name__, url_prefix='/wordmanager')


@bp.route('/')
def index():
    """
    Renders the wordmanager with all the words.
    """
    words = game.get_all_words().get_json()
    return render_template('wordmanager.html', words=words)


@bp.route('/<string:word>', methods=['PUT'])
def put(word):
    """
    This PUT method can be used to add words to the database.
    """
    is_j = has_j(word)
    if is_j is None:
        return make_response(jsonify("this word has no j or ly"), 404)
    else:
        add_to_db(word, is_j=is_j)
        return jsonify(success=True)


@bp.route('/<string:word>', methods=['DELETE'])
def delete(word):
    """
    With this DELETE method we can remove words from the database.
    """
    delete_from_db(word)
    return jsonify(success=True)


def delete_from_db(word):
    cur = db.get_db()
    cur.execute("DELETE FROM word WHERE word=?", (word,))
    cur.commit()


def has_j(word):
    if 'j' in word:
        return 1
    elif 'ly' in word:
        return 0
    else:
        return None


def add_to_db(word, is_j):
    cur = db.get_db()
    try:
        cur.execute("INSERT INTO word (word,is_j) values (?, ?)", (word, is_j))
    except sqlite3.IntegrityError:
        current_app.logger.info('%s is already in the database.', word)
    cur.commit()
