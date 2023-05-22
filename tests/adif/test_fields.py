from adif2json.adif import ParseError, SegmentError, _read_fields, Adif, Record, Reason
import adif2json.parser as par


def test_empty():
    imput = par.stream_character("")
    res = _read_fields(imput)

    assert res == Adif()


def test_qsos():
    imput = "<EOH>\n<QSO_DATE:8>20180101\n<EOR>\n"
    res = _read_fields(par.stream_character(imput))

    assert res is not None
    assert res.headers == Record({})
    assert res.qsos == [Record({"QSO_DATE": "20180101"})]
    assert res.errors is None


def test_headers_only():
    imput = "<PROGRAMID:9>ADIF2JSON\n<PROGRAMVERSION:5>0.0.1\n<EOH>"
    res = _read_fields(par.stream_character(imput))

    assert res == Adif(
        headers=Record({"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"}),
        qsos=None,
        errors=None,
    )


def test_headers_and_qsos():
    imput = """
    <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
    <QSO_DATE:8>20180101<EOR>
    """
    res = _read_fields(par.stream_character(imput))

    assert res == Adif(
        headers=Record({"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"}),
        qsos=[Record({"QSO_DATE": "20180101"})],
        errors=None,
    )


def test_headers_and_qsos_w_tipes():
    imput = """
    <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
    <QSO_DATE:8:S>20180101<EOR>
    """
    res = _read_fields(par.stream_character(imput))

    assert res == Adif(
        headers=Record({"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"}),
        qsos=[Record({"QSO_DATE": "20180101"}, {"QSO_DATE": "S"})],
        errors=None,
    )


def test_headers_and_qsos_compact():
    imput = """
    <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
    <QSO_DATE:8>20180101<EOR>
    """
    res = _read_fields(par.stream_character(imput))

    assert res == Adif(
        headers=Record({"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"}),
        qsos=[Record({"QSO_DATE": "20180101"})],
        errors=None,
    )


def test_headers_and_qsos_bad_size():
    imput = """
        <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
        <CALL:x>EA4HFF<QSO_DATE:8>20180101<EOR>
        """
    res = _read_fields(par.stream_character(imput))

    assert res is not None
    assert res.headers == Record({"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"})
    assert res.qsos == [Record({"QSO_DATE": "20180101"})]
    assert res.errors == [SegmentError(Reason.INVALID_SIZE, 3, 15, 3, 15)]


def test_label_but_value():
    imput = "<CALL:6>"
    res = _read_fields(par.stream_character(imput))

    assert res.headers is None
    assert res.qsos is None
    assert res.errors is not None
    assert len(res.errors) == 1
    err = res.errors[0]
    assert isinstance(err, SegmentError)
    assert err.reason == Reason.TRUNCATED_FILE
    assert err.start_line == 1
    assert err.start_column == 2
    assert err.end_line == 1
    assert err.end_column == 8


def test_no_size_label():
    imput = "<CALL>"
    res = _read_fields(par.stream_character(imput))

    assert res.headers is None
    assert res.qsos is None
    assert res.errors is not None
    assert len(res.errors) == 1
    err = res.errors[0]
    print(err)
    assert isinstance(err, SegmentError)
    assert err.reason == Reason.INVALID_SIZE
    assert err.start_line == 1
    assert err.start_column == 2
    assert err.end_line == 1
    assert err.end_column == 5
