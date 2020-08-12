from hsha.db import get_db
import json


def test_game_sample(app, client):
    """Start with a blank database."""
    with app.app_context():
        db = get_db()
        words = [w[0] for w in db.execute("select word from word").fetchall()]

    rp = client.get('/game/sample/')
    jsonlist = json.loads(rp.data)

    assert words == jsonlist


def test_game_simple_sample(app, client):
    """Start with a blank database."""
    with app.app_context():
        db = get_db()
        words = [w[0] for w in db.execute("select word from word").fetchall()]

    rp = client.get('/game/sample/1')
    jsonlist = json.loads(rp.data)

    assert jsonlist[0] in words
