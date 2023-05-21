from adif2json.parser import Character, stream_character


def test_empty_string():
    assert list(stream_character("")) == []


def test_one_character():
    s = stream_character("a")

    assert next(s) == Character("a", 1, 1)
    assert list(s) == []


def test_two_characters():
    s = stream_character("ab")

    assert next(s) == Character("a", 1, 1)
    assert next(s) == Character("b", 1, 2)
    assert list(s) == []


def test_two_lines():
    s = stream_character("a\nb")

    assert next(s) == Character("a", 1, 1)
    assert next(s) == Character("\n", 2, 0)
    assert next(s) == Character("b", 2, 1)
    assert list(s) == []


def test_two_lines_with_cr():
    s = stream_character("a\r\nb")

    assert next(s) == Character("a", 1, 1)
    assert next(s) == Character("\r", 1, 2)
    assert next(s) == Character("\n", 2, 0)
    assert next(s) == Character("b", 2, 1)
    assert list(s) == []


def test_a_lot_of_chars_and_two_lines():
    a_lot_of_chars = "a" * 1000
    s = stream_character(a_lot_of_chars + "\n" + a_lot_of_chars)

    for i in range(1000):
        assert next(s) == Character("a", 1, i + 1)
    assert next(s) == Character("\n", 2, 0)
    for i in range(1000):
        assert next(s) == Character("a", 2, i + 1)
