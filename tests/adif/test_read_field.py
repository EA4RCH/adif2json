from adif2json.adif import _read_field, Field, Reason


def test_empty():
    imput = ''
    res, _ = _read_field(imput)

    assert res == Reason.EOF
    assert imput == ''


def _check_field(imput, label, tipe, value, rem):
    res, r = _read_field(imput)

    if res and isinstance(res, Field):
        assert res.label == label
        assert res.tipe == tipe
        assert res.value == value
        assert r == rem
    else:
        assert False, 'res is None'


def test_simple_field():
    imput = '<call:6>EA4HFF'
    _check_field(imput, 'call', None, 'EA4HFF', '')


def test_field_w_tipe():
    imput = '<call:6:S>EA4HFF'
    _check_field(imput, 'call', 'S', 'EA4HFF', '')

def test_eof_value():
    imput = '<call:6>EA4'
    res, _ = _read_field(imput)

    assert res == Reason.EOF
    assert imput == '<call:6>EA4'


def test_invalid_label():
    imput = '<:6>EA4HFF'
    res, _ = _read_field(imput)

    assert res == Reason.INVALID_LABEL
    assert imput == '<:6>EA4HFF'


def test_eoh():
    imput = '<eoh>'
    res, rem = _read_field(imput)

    assert res == Reason.EOH
    assert imput == '<eoh>'
    assert rem == ''


def test_exceedent_value():
    imput = '<call:3>EA4HFF<eor>'
    res, rem = _read_field(imput)

    assert res == Reason.EXCEEDENT_VALUE
    assert imput == '<call:3>EA4HFF<eor>'
