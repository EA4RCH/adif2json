from adif2json.adif import _read_label, Label, Reason


def test_empty():
    imput = ''
    res, _ = _read_label(imput)

    assert res == Reason.EOF
    assert imput == ''


def test_no_match():
    imput = 'abc'
    res, _ = _read_label(imput)

    assert res == Reason.EOF
    assert imput == 'abc'


def _check_label(imput, label, size, tipe, rem):
    res = _read_label(imput)

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
    _check_label(imput, 'eof', None, None, '')


def test_match_at_start():
    imput = '<call:6>EA4HFF'
    _check_label(imput, 'call', 6, None, 'EA4HFF')


def test_match_w_tipe():
    imput = '<call:6:S>EA4HFF'
    _check_label(imput, 'call', 6, 'S', 'EA4HFF')


def test_match_w_lower_tipe():
    imput = '<call:6:s>EA4HFF'
    _check_label(imput, 'call', 6, 'S', 'EA4HFF')


def _check_raises(imput):
    res, _ = _read_label(imput)

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
