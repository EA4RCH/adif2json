from adif2json.adif import _read_fields, Adif, Record, Reason
from adif2json.parser import Position


def test_empty():
    imput = Position('')
    res = _read_fields(imput)

    assert res == Adif()


def test_qsos():
    imput = Position('<EOH>\n<QSO_DATE:8>20180101\n<EOR>\n')
    res = _read_fields(imput)

    assert res == Adif(
        headers=Record({}),
        qsos=[Record({'QSO_DATE': '20180101'})],
        errors=None
    )


def test_headers_only():
    imput = Position('<PROGRAMID:9>ADIF2JSON\n<PROGRAMVERSION:5>0.0.1\n<EOH>')
    res = _read_fields(imput)

    assert res == Adif(
        headers=Record({'PROGRAMID': 'ADIF2JSON', 'PROGRAMVERSION': '0.0.1'}),
        qsos=None,
        errors=None
    )


def test_headers_and_qsos():
    imput = Position("""
    <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
    <QSO_DATE:8>20180101<EOR>
    """)
    res = _read_fields(imput)

    assert res == Adif(
        headers=Record({'PROGRAMID': 'ADIF2JSON', 'PROGRAMVERSION': '0.0.1'}),
        qsos=[Record({'QSO_DATE': '20180101'})],
        errors=None
    )


def test_headers_and_qsos_w_tipes():
    imput = Position("""
    <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
    <QSO_DATE:8:S>20180101<EOR>
    """)
    res = _read_fields(imput)

    assert res == Adif(
        headers=Record({'PROGRAMID': 'ADIF2JSON', 'PROGRAMVERSION': '0.0.1'}),
        qsos=[Record({'QSO_DATE': '20180101'}, {'QSO_DATE': 'S'})],
        errors=None
    )


def test_headers_and_qsos_compact():
    imput = Position("""
    <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
    <QSO_DATE:8>20180101<EOR>
    """)
    res = _read_fields(imput)

    assert res == Adif(
        headers=Record({'PROGRAMID': 'ADIF2JSON', 'PROGRAMVERSION': '0.0.1'}),
        qsos=[Record({'QSO_DATE': '20180101'})],
        errors=None
    )


def test_headers_and_qsos_bad_size():
    imput = Position("""
    <PROGRAMID:9>ADIF2JSON<PROGRAMVERSION:5>0.0.1<EOH>
    <CALL:x>EA4HFF<QSO_DATE:8>20180101<EOR>
    """)
    res = _read_fields(imput)

    assert res == Adif(
        headers=Record({'PROGRAMID': 'ADIF2JSON', 'PROGRAMVERSION': '0.0.1'}),
        qsos=[Record({'QSO_DATE': '20180101'})],
        errors=[Reason.INVALID_SIZE]
    )


def test_label_but_value():
    imput = Position('<CALL:6>')
    res = _read_fields(imput)

    assert res == Adif(
        headers=None,
        qsos=None,
        errors=[Reason.TRUNCATED_FILE]
    )


def test_no_size_label():
    imput = Position('<CALL>')
    res = _read_fields(imput)

    assert res == Adif(
        headers=None,
        qsos=None,
        errors=[Reason.INVALID_SIZE]
    )
