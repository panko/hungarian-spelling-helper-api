from flask import Blueprint, session, g, request, render_template, make_response, redirect
from hsha import db
from hsha import game

bp = Blueprint("wordmanager", __name__, url_prefix='/wordmanager')

@bp.route('/')
def index():
    words = game.get_all_words().get_json()
    return render_template('wordmanager.html', words=words)

@bp.route('/<string:word>', methods=['PUT'])
def put(word):
    words = game.get_all_words().get_json()
    return render_template('wordmanager.html', words=words)

@bp.route('/<string:word>', methods=['DELETE'])
def delete(word):
    delete_from_db(word)
    return 0

def delete_from_db(word):
    pass
