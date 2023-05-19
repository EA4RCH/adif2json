from adif2json.parser import _update_position


def test_empty_string():
    string = ""
    pos = _update_position(string, 0, 0)

    assert pos == (0, 0)


def test_only_chars():
    string = "abc"
    pos = _update_position(string, 0, 0)

    assert pos == (1, 4)


def test_only_newlines():
    string = "\n\n\n"
    pos = _update_position(string, 0, 0)

    assert pos == (4, 0)


def test_mixed():
    string = "a\n\n\nb\nc"
    pos = _update_position(string, 0, 0)

    assert pos == (5, 1)
