from flask import Blueprint, jsonify, request, render_template, redirect, g
import random
from hsha import db
from hsha.login import modify_user_score

bp = Blueprint("game", __name__, url_prefix="/game")


@bp.route('/sample/')
def get_all_words():
    '''
    Return every word in our database without modification correctly.
    '''
    data = db.query_db("select word from word")
    data = [v[0] for v in data]
    return jsonify(data)


@bp.route('/sample/<int:numb>')
def get_some_words(numb):
    '''
    Return some of the words in our database without modification correctly.
    numb - number of the retuned words
    '''
    data = db.query_db("select word from word")
    data = [v[0] for v in data]
    return jsonify(random.sample(data, k=numb))


def char_switch_or_not(word):
    '''
    Takes in a word, and with fifty-fifty chance,
    it replaces the 'j's to 'ly's or vica versa.
    Returns the modified word.
    '''
    if random.choice([True, False]):
        if 'j' in word:
            word = word.replace('j', 'ly')
        else:
            word = word.replace('ly', 'j')
    return word


@bp.route('/random/')
def get_one_random():
    '''
    Returns one word with or without modification,
    the chances to get a word with the correct character are 50-50.
    '''
    data = db.query_db("select word, is_j from word")
    word = random.choice([v[0] for v in data])
    word = char_switch_or_not(word)
    return jsonify(word)


@bp.route('/random/<int:numb>')
def get_some_random(numb):
    '''
    Returns 'numb' number of words modificated or not,
    the chances to get a word with the correct character are 50-50.
    numb - number of the retuned words
    '''
    data = db.query_db("select word, is_j from word")
    words = random.sample([v[0] for v in data], k=numb)
    for i, word in enumerate(words):
        words[i] = char_switch_or_not(word)
    return jsonify(words)


@bp.route('/validate', methods=['POST'])
def validate():
    score = 0
    request_json = request.get_json(force=True)
    words = request_json['words']
    is_checked = request_json['is_checked']
    if not len(words) == len(is_checked):
        return jsonify(-1)
    valid_words = [v[0] for v in db.query_db("select word from word")]

    for i, word in enumerate(words):
        if is_checked[i]:
            if word in valid_words:
                score = score + 1
        else:
            if word in valid_words:
                score = score - 1
            else:
                score = score + 1
    if g.user:
        modify_user_score(g.user['username'], score)
    return jsonify(score)


@bp.route('/', methods=['POST', 'GET'])
def game_webpage():
    if request.method == 'GET':
        return redirect("/")
    rounds_count = int(request.form['rounds_count'])
    words = get_some_random(rounds_count).get_json()
    return render_template('game.html', words=words)
