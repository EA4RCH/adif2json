from adif2json.parser import read_until, read_forward


def test_read_empty():
    imput = '' # the input must be reamaing the same
    res_until, _ = read_until(imput, 'a')
    res_forward, _ = read_forward(imput,'a')

    assert res_until == ''
    assert res_forward == ''


def test_no_match():
    imput = 'abc' # the input must be reamaing the same
    res_until, rem_until = read_until(imput, 'd')
    res_forward, rem_forward = read_forward(imput,'d')

    assert res_until == 'abc'
    assert rem_until == ''
    assert res_forward == 'abc'
    assert rem_forward == ''


def test_match_at_start():
    imput = 'abc' # the input must be reamaing the same
    res_until, rem_until = read_until(imput, 'a')
    res_forward, rem_forward = read_forward(imput,'a')

    assert res_until == ''
    assert rem_until == 'abc'
    assert res_forward == 'a'
    assert rem_forward == 'bc'


def test_match_at_end():
    imput = 'abc' # the input must be reamaing the same
    res_until, rem_until = read_until(imput, 'c')
    res_forward, rem_forward = read_forward(imput,'c')

    assert res_until == 'ab'
    assert rem_until == 'c'
    assert res_forward == 'abc'
    assert rem_forward == ''


def test_match_at_middle():
    imput = 'abc' # the input must be reamaing the same
    res_until, rem_until = read_until(imput, 'b')
    res_forward, rem_forward = read_forward(imput,'b')

    assert res_until == 'a'
    assert rem_until == 'bc'
    assert res_forward == 'ab'
    assert rem_forward == 'c'


def test_match_multiple_chars():
    imput = 'abc' # the input must be reamaing the same
    res_until, rem_until = read_until(imput, 'a', 'b')
    res_forward, rem_forward = read_forward(imput,'a', 'b')

    assert res_until == ''
    assert rem_until == 'abc'
    assert res_forward == 'a'
    assert rem_forward == 'bc'


def test_match_multiple_chars_at_middle():
    imput = 'abc' # the input must be reamaing the same
    res_until, rem_until = read_until(imput, 'b', 'c')
    res_forward, rem_forward = read_forward(imput, 'b', 'c')

    assert res_until == 'a'
    assert rem_until == 'bc'
    assert res_forward == 'ab'
    assert rem_forward == 'c'
