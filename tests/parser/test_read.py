from adif2json.parser import read_until, read_forward, Position, EndOfFile


def test_read_empty():
    imput = Position("")
    res_until = read_until(imput, "a")
    res_forward = read_forward(imput, "a")

    assert res_until == ("", EndOfFile(1, 1))
    assert res_forward == ("", EndOfFile(1, 1))


def test_no_match():
    imput = Position("abc")
    res_until = read_until(imput, "d")
    res_forward = read_forward(imput, "d")

    assert res_until == ("abc", EndOfFile(1, 4))
    assert res_forward == ("abc", EndOfFile(1, 4))


def _check_no_eof_value(imput, val, rem, fun, c, lin, col):
    res = fun(Position(imput), c)
    print(res)
    assert res == (val, Position(rem, lin, col))


def test_match_at_start():
    imput = "abc"
    _check_no_eof_value(imput, "", "abc", read_until, "a", 1, 1)
    _check_no_eof_value(imput, "a", "bc", read_forward, "a", 1, 2)
    assert imput == "abc"


def test_match_at_end():
    imput = "abc"
    _check_no_eof_value(imput, "ab", "c", read_until, "c", 1, 3)
    _check_no_eof_value(imput, "abc", "", read_forward, "c", 1, 4)
    assert imput == "abc"


def test_match_at_middle():
    imput = "abc"
    _check_no_eof_value(imput, "a", "bc", read_until, "b", 1, 2)
    _check_no_eof_value(imput, "ab", "c", read_forward, "b", 1, 3)
    assert imput == "abc"


def test_correct_line_numbers():
    imput = "a\n\n\nb\nc"
    res_until = read_until(Position(imput), "b")

    assert res_until == ("a\n\n\n", Position("b\nc", 4, 0))
