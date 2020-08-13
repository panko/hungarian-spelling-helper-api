import json
import unittest


def test_game_sample(db_words, client):
    """GET /game/sample. It has to return
    all of the qords form the db as json."""
    db_words = db_words()
    rp = client.get('/game/sample/')
    jsonlist = json.loads(rp.data)

    assert db_words == jsonlist


def test_game_simple_sample_one(db_words, client):
    """GET /game/sample/<int>
    It should return the specified number of words from the db randomly."""
    db_words = db_words()
    rp = client.get('/game/sample/1')
    jsonlist = json.loads(rp.data)

    assert len(jsonlist) == 1
    assert jsonlist[0] in db_words


def test_game_simple_sample_100(db_words, client):
    """GET /game/sample/100
    It should return the specified number of words from the db randomly."""
    db_words = db_words()
    rp = client.get('/game/sample/100')
    jsonlist = json.loads(rp.data)

    assert len(jsonlist) == 100
    for word in jsonlist:
        assert word in db_words


def test_game_simple_sample_1000(db_words, client):
    """GET /game/sample/1000
    This test is tricky, because normally we dont have 1000 item in our db.
    It should return it should return a 404 page."""
    rp = client.get('/game/sample/1000')

    assert rp.status_code == 404


def test_game_simple_sample_minus(db_words, client):
    """GET /game/sample/-1
    TIt doesnt make sense to return minus one from a list
    It should return a 404 error page."""
    rp = client.get('/game/sample/-1')

    assert rp.status_code == 404


def test_game_random(db_words, client):
    """GET /game/random
    It should return one word from the db,
    with or without the right spelling."""
    db_words = db_words()
    rp = client.get('/game/random/')
    word = json.loads(rp.data)

    assert (word in db_words) or (switch_j_ly(word) in db_words)


def test_game_randoms_one(db_words, client):
    """GET /game/randoms/<integer>
    Basically the same as the one above, but on another endpoint.
    The difference is here that we expect as list of words, not a single one.
    """
    db_words = db_words()
    rp = client.get('/game/randoms/1')
    jsonlist = json.loads(rp.data)

    for word in jsonlist:
        assert (word in db_words) or (switch_j_ly(word) in db_words)


def test_game_randoms_ten(db_words, client):
    """GET /game/randoms/<integer>
    Basically the same as the one above, but on another endpoint.
    """
    db_words = db_words()
    rp = client.get('/game/randoms/10')
    jsonlist = json.loads(rp.data)

    for word in jsonlist:
        assert (word in db_words) or (switch_j_ly(word) in db_words)


def test_game_randoms_1000(client):
    """GET /game/randoms/1000
    Test what happens if we dont have that much item in our db.
    It should return a 404.
    """
    rp = client.get('/game/randoms/1000')
    assert rp.status_code == 404


def test_game_randoms_minus(client):
    """GET /game/randoms/-2
    Test what happens if we supply negative number to the API.
    It should return a 404.
    """
    rp = client.get('/game/randoms/-2')
    assert rp.status_code == 404


def test_game_validate(client):
    """POST /game/validate
    It's used to get our score from the sent data. Test a simple example.
    """
    rp = client.post('/game/validate', content_type='application/json',
    data='{"words":["hélya","borbéj","olaj","lyuhász","relyt"],"is_checked":[false,false,true,false,false]}')
    assert rp.status_code == 200
    assert int(rp.data) == 5


def test_game_validate_negative(client):
    """POST /game/validate
    It's used to get our score from the sent data. Test a simple example.
    """
    rp = client.post('/game/validate', content_type='application/json',
    data='{"words":["hélya","borbéj","olaj","lyuhász","relyt"],"is_checked":[true,true,false,true,true]}')
    assert rp.status_code == 200
    assert int(rp.data) == -5

# HELPERS
def switch_j_ly(word):
    if 'j' in word:
        res = word.replace('j', 'ly')
    else:
        res = word.replace('ly', 'j')
    assert word != res
    return res
