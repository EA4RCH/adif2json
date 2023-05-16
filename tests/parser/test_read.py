from adif2json.parser import read_until, read_forward, Position, EndOfFile


def test_read_empty():
    imput = Position('')
    res_until = read_until(imput, 'a')
    res_forward = read_forward(imput,'a')

    assert res_until == ('', EndOfFile(1, 1))
    assert res_forward == ('', EndOfFile(1, 1))


def test_no_match():
    imput = Position('abc')
    res_until = read_until(imput, 'd')
    res_forward = read_forward(imput,'d')

    assert res_until == ('abc', EndOfFile(1, 4))
    assert res_forward == ('abc', EndOfFile(1, 4))


def _check_no_eof_value(imput, val, rem, fun, c):
    res = fun(Position(imput), c)

    assert res == (val, Position(rem, 1, len(val) + 1))

def test_match_at_start():
    imput = 'abc'
    _check_no_eof_value(imput, '', 'abc', read_until, 'a')
    _check_no_eof_value(imput, 'a', 'bc', read_forward, 'a')
    assert imput == 'abc'


def test_match_at_end():
    imput = 'abc'
    _check_no_eof_value(imput, 'ab', 'c', read_until, 'c')
    _check_no_eof_value(imput, 'abc', '', read_forward, 'c')
    assert imput == 'abc'


def test_match_at_middle():
    imput = 'abc'
    _check_no_eof_value(imput, 'a', 'bc', read_until, 'b')
    _check_no_eof_value(imput, 'ab', 'c', read_forward, 'b')
    assert imput == 'abc'
