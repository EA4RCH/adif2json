from adif2json.parser import read_n, Position, EndOfFile


def test_read_empty():
    imput = Position('')
    res = read_n(imput, 1)

    assert res == ('', EndOfFile(1, 1))


def test_read_zero():
    imput = Position('abc')
    res = read_n(imput, 0)

    assert res == ('', Position('abc', 1, 1))


def test_read_one():
    imput = Position('abc')
    res = read_n(imput, 1)

    assert res == ('a', Position('bc', 1, 2))


def test_read_two():
    imput = Position('abc')
    res = read_n(imput, 2)

    assert res == ('ab', Position('c', 1, 3))


def test_read_more_than_string():
    imput = Position('abc')
    res = read_n(imput, 4)

    assert res == ('abc', EndOfFile(1, 4))


def test_unicode():
    imput = Position("ĀBC")
    res = read_n(imput, 2)

    assert res == ('ĀB', Position('C', 1, 3))
