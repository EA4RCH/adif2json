from adif2json.parser import discard_until, discard_forward, \
    Position, EndOfFile


def test_empty_string():
    imp = Position("")
    res_until = discard_until(imp, "a")
    res_forward = discard_forward(imp, "a")
    assert res_until == EndOfFile(1, 1)
    assert res_forward == EndOfFile(1, 1)


def test_no_match():
    imp = Position("abc")
    res_until = discard_until(imp, "d")
    res_forward = discard_forward(imp, "d")
    assert res_until == EndOfFile(1, 4)
    assert res_forward == EndOfFile(1, 4)


def test_match_at_start():
    imp = Position("abc")
    res_until = discard_until(imp, "a")
    res_forward = discard_forward(imp, "a")
    assert res_until == Position("abc", 1, 1)
    assert res_forward == Position("bc", 1, 2)


def test_match_at_end():
    imp = Position("abc")
    res_until = discard_until(imp, "c")
    res_forward = discard_forward(imp, "c")
    assert res_until == Position("c", 1, 3)
    assert res_forward == Position("", 1, 4)


def test_match_in_middle():
    imp = Position("abc")
    res_until = discard_until(imp, "b")
    res_forward = discard_forward(imp, "b")
    assert res_until == Position("bc", 1, 2)
    assert res_forward == Position("c", 1, 3)
