from adif2json.adif import ParseError, SegmentError, _read_fields, Adif, Record, Reason
import adif2json.parser as par


def test_empty():
    imput = par.stream_character("")
    res_l = list(_read_fields(imput))

    assert res_l == []


def test_qsos():
    imput = "<EOH>\n<QSO_DATE:8>20180101\n<EOR>\n"
    res_l = list(_read_fields(par.stream_character(imput)))

    assert len(res_l) == 2
    res = res_l[0]
    assert res.type == "headers"
    assert res.fields == {}
    assert res.errors is None
    res = res_l[1]
    assert res.type == "qso"
    assert len(res.fields) == 1
    assert res.fields == {"QSO_DATE": "20180101"}
    assert res.errors is None


def test_headers_only():
    imput = "<PROGRAMID:9>ADIF2JSON\n<PROGRAMVERSION:5>0.0.1\n<EOH>"
    res_l = list(_read_fields(par.stream_character(imput)))

    assert len(res_l) == 1
    res = res_l[0]
    assert res.type == "headers"
    assert res.fields == {"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"}
    assert res.errors is None


def test_headers_and_qsos():
    imput = """
    <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
    <QSO_DATE:8>20180101<EOR>
    """
    res_l = list(_read_fields(par.stream_character(imput)))

    assert len(res_l) == 2
    res = res_l[0]
    assert res.type == "headers"
    assert res.fields == {"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"}
    assert res.errors is None
    res = res_l[1]
    assert res.type == "qso"
    assert len(res.fields) == 1
    assert res.fields == {"QSO_DATE": "20180101"}
    assert res.errors is None


def test_headers_and_qsos_w_tipes():
    imput = """
    <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
    <QSO_DATE:8:S>20180101<EOR>
    """
    res_l = list(_read_fields(par.stream_character(imput)))

    assert len(res_l) == 2
    res = res_l[0]
    assert res.type == "headers"
    assert res.fields == {"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"}
    assert res.errors is None
    res = res_l[1]
    assert res.type == "qso"
    assert len(res.fields) == 1
    assert res.fields == {"QSO_DATE": "20180101"}
    assert res.errors is None


def test_headers_and_qsos_compact():
    imput = """
    <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
    <QSO_DATE:8>20180101<EOR>
    """
    res_l = list(_read_fields(par.stream_character(imput)))

    assert len(res_l) == 2
    res = res_l[0]
    assert res.type == "headers"
    assert res.fields == {"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"}
    assert res.errors is None
    res = res_l[1]
    assert res.type == "qso"
    assert len(res.fields) == 1
    assert res.fields == {"QSO_DATE": "20180101"}


def test_headers_and_qsos_bad_size():
    imput = """
        <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
        <CALL:x>EA4HFF<QSO_DATE:8>20180101<EOR>
        """
    res_l = list(_read_fields(par.stream_character(imput)))

    assert len(res_l) == 2
    res = res_l[0]
    assert res.type == "headers"
    assert res.fields == {"PROGRAMID": "ADIF2JSON", "PROGRAMVERSION": "0.0.1"}
    assert res.errors is None
    res = res_l[1]
    assert res.type == "qso"
    assert len(res.fields) == 1
    assert res.fields == {"QSO_DATE": "20180101"}
    assert res.errors is not None
    assert len(res.errors) == 1
    err = res.errors[0]
    print(err)
    assert err["reason"] == Reason.INVALID_SIZE.name
    assert err["start_line"] == 3
    assert err["start_column"] == 15
    assert err["end_line"] == 3
    assert err["end_column"] == 15


def test_label_but_value():
    imput = "<CALL:6>"
    res_l = list(_read_fields(par.stream_character(imput)))

    assert len(res_l) == 1
    res = res_l[0]
    assert res.type == "qso"
    assert res.fields == {}
    assert res.errors is not None
    assert len(res.errors) == 1
    err = res.errors[0]
    print(err)
    assert err["reason"] == Reason.TRUNCATED_FILE.name
    assert err["start_line"] == 1
    assert err["start_column"] == 2
    assert err["end_line"] == 1
    assert err["end_column"] == 8


def test_no_size_label():
    imput = "<CALL>"
    res_l = list(_read_fields(par.stream_character(imput)))

    assert len(res_l) == 1
    res = res_l[0]
    assert res.type == "qso"
    assert res.fields == {}
    assert res.errors is not None
    assert len(res.errors) == 1
    err = res.errors[0]
    assert err["reason"] == Reason.INVALID_SIZE.name
    assert err["start_line"] == 1
    assert err["start_column"] == 2
    assert err["end_line"] == 1
    assert err["end_column"] == 5
