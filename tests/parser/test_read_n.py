from adif2json.parser import read_n


def test_read_empty():
    imput = '' # the input must be reamaing the same
    res = read_n(imput, 1)

    assert res is None
    assert imput == ''


def test_read_zero():
    imput = 'abc' # the input must be reamaing the same
    res, rem = read_n(imput, 0)

    assert res == ''
    assert rem == 'abc'
    assert imput == 'abc'


def test_read_one():
    imput = 'abc' # the input must be reamaing the same
    res, rem = read_n(imput, 1)

    assert res == 'a'
    assert rem == 'bc'
    assert imput == 'abc'


def test_read_two():
    imput = 'abc' # the input must be reamaing the same
    res, rem = read_n(imput, 2)

    assert res == 'ab'
    assert rem == 'c'
    assert imput == 'abc'


def test_read_more_than_string():
    imput = 'abc' # the input must be reamaing the same
    res = read_n(imput, 4)

    assert res is None
    assert imput == 'abc'
