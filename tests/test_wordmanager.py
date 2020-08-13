def test_wormanager_put(db_words, client):
    """

    """
    word = 'ajajaj'
    assert word not in db_words()
    rp = client.put("/wordmanager/{}".format(word))
    assert rp.status_code == 200

    words = db_words()

    assert word in words



def test_wormanager_delete(client, db_words):
    """

    """
    word = 'ajaj'
    assert word not in db_words()
    client.put("/wordmanager/{}".format(word))
    assert word in db_words()
    rp = client.delete("/wordmanager/{}".format(word))
    assert word not in db_words()

    assert rp.status_code == 200


def test_wormanager_put_twotimes():
    """

    """
    pass


def test_wormanager_put_invalid():
    """

    """
    pass

