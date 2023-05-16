from adif2json.adif import _read_field, Field, Reason
from adif2json.parser import Position, EndOfFile


def test_empty():
    imput = Position('')
    res, rem = _read_field(imput)

    assert res == Reason.EOF
    assert rem == EndOfFile(1, 1)


def _check_field(imput, label, tipe, value, rem):
    res, r = _read_field(Position(imput))

    if res and isinstance(res, Field):
        assert res.label == label
        assert res.tipe == tipe
        assert res.value == value
        assert r == rem
    else:
        assert False, 'res is None'


def test_simple_field():
    imput = '<call:6>EA4HFF'
    _check_field(imput, 'call', None, 'EA4HFF', EndOfFile(1, 15))


def test_field_w_tipe():
    imput = '<call:6:S>EA4HFF'
    _check_field(imput, 'call', 'S', 'EA4HFF', EndOfFile(1, 17))

def test_eof_value():
    imput = '<call:6>EA4'
    res, rem = _read_field(Position(imput))

    assert res == Reason.EOF
    assert rem == EndOfFile(1, 12)


def test_invalid_label():
    imput = '<:6>EA4HFF'
    res, rem = _read_field(Position(imput))

    assert res == Reason.INVALID_LABEL
    assert rem == Position('EA4HFF', 1, 5)


def test_eoh():
    imput = '<eoh>'
    res, rem = _read_field(Position(imput))

    assert res == Reason.EOH
    assert imput == '<eoh>'
    assert rem == Position('', 1, 6)


def test_exceedent_value():
    imput = '<call:3>EA4HFF<eor>'
    res, rem = _read_field(Position(imput))

    assert res == Reason.EXCEEDENT_VALUE
    assert imput == '<call:3>EA4HFF<eor>'
