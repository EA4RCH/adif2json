from adif2json.parser import read_until, read_forward


def test_read_empty():
    imput = ''
    res_until = read_until(imput, 'a')
    res_forward = read_forward(imput,'a')

    assert res_until is None
    assert res_forward is None
    assert imput == ''


def test_no_match():
    imput = 'abc'
    res_until = read_until(imput, 'd')
    res_forward = read_forward(imput,'d')

    assert res_until is None
    assert res_forward is None
    assert imput == 'abc'


def _check_no_eof_value(imput, val, rem, fun, *chars):
    res = fun(imput, *chars)
    if res:
        val, rem = res
        assert val == val
        assert rem == rem
    else:
        assert False


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


def test_match_multiple_chars():
    imput = 'abc'
    _check_no_eof_value(imput, '', 'abc', read_until, 'a', 'b')
    _check_no_eof_value(imput, 'a', 'bc', read_forward, 'a', 'b')
    assert imput == 'abc'


def test_match_multiple_chars_at_middle():
    imput = 'abc'
    _check_no_eof_value(imput, 'a', 'bc', read_until, 'b', 'c')
    _check_no_eof_value(imput, 'ab', 'c', read_forward, 'b', 'c')
    assert imput == 'abc'
