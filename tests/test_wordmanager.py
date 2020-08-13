def test_wormanager_put(db_words, client):
    """
    PUT /wordmanager/<string>
    I should add the word to the db and return with a 200.
    """
    word = 'ajajaj'
    assert word not in db_words()
    rp = client.put("/wordmanager/{}".format(word))
    assert rp.status_code == 200

    words = db_words()

    assert word in words


def test_wormanager_delete(client, db_words):
    """
    DELETE /wordmanager/<string>
    I should delete a word from the db and return with  successfull 200.
    """
    word = 'ajaj'
    assert word not in db_words()
    client.put("/wordmanager/{}".format(word))
    assert word in db_words()
    rp = client.delete("/wordmanager/{}".format(word))
    assert word not in db_words()

    assert rp.status_code == 200


def test_wormanager_put_twotimes(client, db_words):
    """
    PUT /wordmanager/<string>
    If we try to put two times the same word,
    we should get back a regular success with 200.
    """
    word = 'ajaj'
    assert word not in db_words()
    client.put("/wordmanager/{}".format(word))
    rp = client.put("/wordmanager/{}".format(word))

    assert word in db_words()
    assert rp.status_code == 200


def test_wormanager_put_invalid(client, db_words):
    """
    PUT /wordmanager/<string>
    If we try to put an invalid word into the db,
    we should get back a 400 statuscode,
    and the word shouldnt appear in the db.
    """
    word = 'nincsbenneerdekeskarakter'
    assert word not in db_words()
    client.put("/wordmanager/{}".format(word))
    rp = client.put("/wordmanager/{}".format(word))

    assert word not in db_words()
    assert rp.status_code == 400
    assert '"this word has no j or ly"\n' == rp.data.decode('utf-8')


def test_wormanager_delete_notexistent(client, db_words):
    """
    DELETE /wordmanager/<string>
    If we try to delete a word what is not in the db,
    we should get back a regular success with 200.
    If it's not there then we are good.
    """
    word = 'thisisntindb'
    assert word not in db_words()
    rp = client.delete("/wordmanager/{}".format(word))
    assert word not in db_words()
    assert rp.status_code == 200


def test_wormanager_put_hungarian(db_words, client):
    """
    PUT /wordmanager/<string>
    I should add the word to the db and return with a 200.
    """
    word = 'árvíztűrőtükörfúrógépjaja'
    assert word not in db_words()
    rp = client.put("/wordmanager/{}".format(word))
    assert rp.status_code == 200

    words = db_words()

    assert word in words
