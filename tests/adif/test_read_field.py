from adif2json.adif import _read_field, Field


def test_empty():
    imput = ''
    res, _ = _read_field(imput)

    assert res is None
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


def test_eoh():
    imput = '<eoh>'
    _check_field(imput, 'eoh', None, None, '')

def test_eof_value():
    imput = '<call:6>EA4'
    res, _ = _read_field(imput)

    assert res is None
    assert imput == '<call:6>EA4'


def test_invalid_label():
    imput = '<:6>EA4HFF'
    res, _ = _read_field(imput)

    assert isinstance(res, str)
    assert imput == '<:6>EA4HFF'
