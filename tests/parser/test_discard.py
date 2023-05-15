from adif2json.parser import discard_until, discard_forward


def test_empty_string():
    res_until = discard_until("", "a")
    res_forward = discard_forward("", "a")
    assert res_until == ""
    assert res_forward == ""


def test_no_match():
    res_until = discard_until("abc", "d")
    res_forward = discard_forward("abc", "d")
    assert res_until == ""
    assert res_forward == ""


def test_match_at_start():
    res_until = discard_until("abc", "a")
    res_forward = discard_forward("abc", "a")
    assert res_until == "abc"
    assert res_forward == "bc"


def test_match_at_end():
    res_until = discard_until("abc", "c")
    res_forward = discard_forward("abc", "c")
    assert res_until == "c"
    assert res_forward == ""


def test_match_in_middle():
    res_until = discard_until("abc", "b")
    res_forward = discard_forward("abc", "b")
    assert res_until == "bc"
    assert res_forward == "c"


def test_match_multiple_chars():
    res_until = discard_until("abc", "b", "c")
    res_forward = discard_forward("abc", "b", "c")
    assert res_until == "bc"
    assert res_forward == "c"


def test_match_multiple_chars_in_middle():
    res_until = discard_until("abc", "c", "b")
    res_forward = discard_forward("abc", "c", "b")
    assert res_until == "bc"
    assert res_forward == "c"
