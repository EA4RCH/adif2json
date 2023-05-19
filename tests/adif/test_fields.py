from adif2json.adif import ParseError, SegmentError, _read_fields, Adif, Record, Reason
from adif2json.parser import Position


def test_empty():
    imput = Position("")
    res = _read_fields(imput)

    assert res == Adif()


def test_qsos():
    imput = Position("<EOH>\n<QSO_DATE:8>20180101\n<EOR>\n")
    res = _read_fields(imput)

    assert res == Adif(
        headers=Record({}), qsos=[Record({"QSO_DATE": "20180101"})], errors=None
    )


def test_headers_only():
    imput = Position("<PROGRAMID:9>ADIF2JSON\n<PROGRAMVERSION:5>0.0.1\n<EOH>")
    res = _read_fields(imput)

    assert res == Adif(
        headers=Record({"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"}),
        qsos=None,
        errors=None,
    )


def test_headers_and_qsos():
    imput = Position(
        """
    <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
    <QSO_DATE:8>20180101<EOR>
    """
    )
    res = _read_fields(imput)

    assert res == Adif(
        headers=Record({"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"}),
        qsos=[Record({"QSO_DATE": "20180101"})],
        errors=None,
    )


def test_headers_and_qsos_w_tipes():
    imput = Position(
        """
    <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
    <QSO_DATE:8:S>20180101<EOR>
    """
    )
    res = _read_fields(imput)

    assert res == Adif(
        headers=Record({"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"}),
        qsos=[Record({"QSO_DATE": "20180101"}, {"QSO_DATE": "S"})],
        errors=None,
    )


def test_headers_and_qsos_compact():
    imput = Position(
        """
    <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
    <QSO_DATE:8>20180101<EOR>
    """
    )
    res = _read_fields(imput)

    assert res == Adif(
        headers=Record({"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"}),
        qsos=[Record({"QSO_DATE": "20180101"})],
        errors=None,
    )


def test_headers_and_qsos_bad_size():
    imput = Position(
        """
        <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
        <CALL:x>EA4HFF<QSO_DATE:8>20180101<EOR>
        """
    )
    res = _read_fields(imput)

    print(res.errors)
    assert res is not None
    assert res.headers == Record({"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"})
    assert res.qsos == [Record({"QSO_DATE": "20180101"})]
    assert res.errors == [SegmentError(Reason.INVALID_SIZE, 3, 13, 1)]


def test_label_but_value():
    imput = Position("<CALL:6>")
    res = _read_fields(imput)

    assert res.headers is None
    assert res.qsos is None
    assert res.errors is not None
    assert len(res.errors) == 1
    err = res.errors[0]
    assert isinstance(err, ParseError)
    assert err.reason == Reason.TRUNCATED_FILE
    assert err.line == 1
    assert err.column == 9


def test_no_size_label():
    imput = Position("<CALL>")
    res = _read_fields(imput)

    assert res.headers is None
    assert res.qsos is None
    assert res.errors is not None
    assert len(res.errors) == 1
    err = res.errors[0]
    assert isinstance(err, ParseError)
    assert err.reason == Reason.INVALID_SIZE
    assert err.line == 1
    assert err.column == 6
