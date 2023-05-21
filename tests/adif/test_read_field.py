from adif2json.adif import ParseError, SegmentError, _read_field, Field, Reason
import adif2json.parser as p


def test_empty():
    imput = p.stream_character("")
    res = list(_read_field(imput))

    assert len(res) == 0


def _check_field(imput, label, tipe, value):
    imp = p.stream_character(imput)
    res = list(_read_field(imp))

    assert len(res) == 1
    if res[0] and isinstance(res, Field):
        assert res.label == label
        assert res.tipe == tipe
        assert res.value == value


def test_simple_field():
    imput = "<call:6>EA4HFF"
    _check_field(imput, "call", None, "EA4HFF")


def test_field_w_tipe():
    imput = "<call:6:S>EA4HFF"
    _check_field(imput, "call", "S", "EA4HFF")


def test_eof_value():
    imput = p.stream_character("<call:6>EA4")
    res_l = list(_read_field(imput))

    assert len(res_l) == 1, "expected 1 result, got {}".format(len(res_l))
    res = res_l[0]
    assert isinstance(res, SegmentError)
    assert res.reason == Reason.TRUNCATED_FILE
    assert res.start_line == 1
    assert res.start_column == 2
    assert res.end_line == 1
    assert res.end_column == 11


def test_invalid_label():
    imput = p.stream_character("<:6>EA4HFF")
    res_l = list(_read_field(imput))

    assert len(res_l) == 1, "expected 1 result, got {}".format(len(res_l))
    res = res_l[0]
    assert isinstance(res, ParseError)
    assert res.reason == Reason.INVALID_LABEL
    assert res.line == 1
    assert res.column == 2


def test_eoh():
    imput = p.stream_character("<eoh>")
    res = list(_read_field(imput))

    assert len(res) == 1
    assert res[0] == Reason.EOH


def test_exceedent_value():
    imput = p.stream_character("<call:3>EA4HFF<eor>")
    res_l = list(_read_field(imput))

    assert len(res_l) == 3
    res = res_l[0]
    assert isinstance(res, Field)
    assert res.label == "call"
    assert res.tipe is None
    assert res.value == "EA4"
    res = res_l[1]
    assert isinstance(res, SegmentError)
    assert res.reason == Reason.EXCEEDENT_VALUE
    assert res.start_line == 1
    assert res.start_column == 12
    assert res.end_line == 1
    assert res.end_column == 14
    res = res_l[2]
    assert isinstance(res, Reason)
    assert res == Reason.EOR


def test_truncated_label():
    imput = p.stream_character("<call:6")
    res_l = list(_read_field(imput))

    assert len(res_l) == 1
    res = res_l[0]
    assert isinstance(res, SegmentError)
    assert res.reason == Reason.INVALID_SIZE
    assert res.start_line == 1
    assert res.start_column == 7
    assert res.end_line == 1
    assert res.end_column == 8


def test_zero_size_label():
    imput = p.stream_character("<call:0> ")
    res_l = list(_read_field(imput))

    assert len(res_l) == 1
    res = res_l[0]
    assert isinstance(res, Field)
    assert res.label == "call"
    assert res.tipe is None
    assert res.value == ""
