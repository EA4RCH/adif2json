from adif2json.adif import ParseError, SegmentError, _read_field, Field, Reason
from adif2json.parser import Position, EndOfFile


def test_empty():
    imput = Position("")
    res, rem = _read_field(imput)

    assert isinstance(res, ParseError)
    assert res.reason == Reason.EOF
    assert res.line == 1
    assert res.column == 1
    assert rem == EndOfFile(1, 1)


def _check_field(imput, label, tipe, value, rem):
    res, r = _read_field(Position(imput))

    if res and isinstance(res, Field):
        assert res.label == label
        assert res.tipe == tipe
        assert res.value == value
        assert r == rem
    else:
        assert False, "res is None"


def test_simple_field():
    imput = "<call:6>EA4HFF"
    _check_field(imput, "call", None, "EA4HFF", EndOfFile(1, 15))


def test_field_w_tipe():
    imput = "<call:6:S>EA4HFF"
    _check_field(imput, "call", "S", "EA4HFF", EndOfFile(1, 17))


def test_eof_value():
    imput = "<call:6>EA4"
    res, rem = _read_field(Position(imput))

    assert isinstance(res, ParseError)
    assert res.reason == Reason.TRUNCATED_FILE
    assert res.line == 1
    assert res.column == 12
    assert rem == EndOfFile(1, 12)


def test_invalid_label():
    imput = "<:6>EA4HFF"
    res, rem = _read_field(Position(imput))

    assert isinstance(res, SegmentError)
    assert res.reason == Reason.INVALID_LABEL
    assert res.line == 1
    assert res.column == 2
    assert res.size == 1
    assert rem == Position("EA4HFF", 1, 5)


def test_eoh():
    imput = "<eoh>"
    res, rem = _read_field(Position(imput))

    assert isinstance(res, ParseError)
    assert res.reason == Reason.EOH
    assert res.line == 1
    assert res.column == 6
    assert rem == Position("", 1, 6)


def test_exceedent_value():
    imput = "<call:3>EA4HFF<eor>"
    res, _ = _read_field(Position(imput))

    assert isinstance(res, SegmentError)
    assert res.reason == Reason.EXCEEDENT_VALUE
    assert res.line == 1
    assert res.column == 12
    assert res.size == 3


def test_truncated_label():
    imput = "<call:6"
    res, rem = _read_field(Position(imput))

    assert isinstance(res, SegmentError)
    assert res.reason == Reason.INVALID_LABEL
    assert res.line == 1
    assert res.column == 1
    assert res.size == 7
    assert rem == EndOfFile(1, 8)
