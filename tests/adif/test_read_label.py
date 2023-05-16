from adif2json.adif import _read_label, Label, Reason
from adif2json.parser import Position, EndOfFile


def test_empty():
    imput = Position('')
    _, rem = _read_label(imput)

    assert rem == EndOfFile(1, 1)


def test_no_match():
    imput = Position('abc')
    _, rem = _read_label(imput)

    assert rem == EndOfFile(1, 4)


def _check_label(imput, label, size, tipe, rem):
    res = _read_label(Position(imput))

    l, r = res
    if isinstance(l, Label):
        assert l.label == label
        assert l.size == size
        assert l.tipe == tipe
    else:
        assert False, 'label is not a Label'
    assert r == rem


def test_eof_label():
    imput = '<EOF>'
    _check_label(imput, 'EOF', None, None, Position('', 1, 6))


def test_match_at_start():
    imput = '<call:6>EA4HFF'
    _check_label(imput, 'call', 6, None, Position('EA4HFF', 1, 9))


def test_match_w_tipe():
    imput = '<call:6:S>EA4HFF'
    _check_label(imput, 'call', 6, 'S', Position('EA4HFF', 1, 11))


def test_match_w_lower_tipe():
    imput = '<call:6:s>EA4HFF'
    _check_label(imput, 'call', 6, 's', Position('EA4HFF', 1, 11))


def _check_raises(imput):
    res, _ = _read_label(Position(imput))

    assert isinstance(res, Reason), res


def test_invalid_label():
    imput = '<>EA4HFF'
    _check_raises(imput)


def test_invalid_size():
    imput = '<call:6a>EA4HFF'
    _check_raises(imput)


def test_invalid_tipe():
    imput = '<call:6:9>EA4HFF'
    _check_raises(imput)


def test_empty_label_w_size():
    imput = '<:6>EA4HFF'
    _check_raises(imput)


def test_empty_size():
    imput = '<call:>EA4HFF'
    _check_raises(imput)


def test_empty_tipe():
    imput = '<call:6:>EA4HFF'
    _check_raises(imput)
