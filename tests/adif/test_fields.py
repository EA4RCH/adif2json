from adif2json.adif import _read_fields, Adif, Record
from adif2json.parser import Position


def test_empty():
    imput = Position('')
    res = _read_fields(imput)

    assert res == Adif()


def test_qsos():
    imput = Position('<EOH>\n<QSO_DATE:8>20180101\n<EOR>\n')
    res = _read_fields(imput)

    assert res == Adif(headers=Record({}), qsos=[Record({'QSO_DATE': '20180101'})], errors=None)


def test_headers_only():
    imput = Position('<PROGRAMID:9>ADIF2JSON\n<PROGRAMVERSION:5>0.0.1\n<EOH>')
    res = _read_fields(imput)

    assert res == Adif(headers=Record({'PROGRAMID': 'ADIF2JSON', 'PROGRAMVERSION': '0.0.1'}), qsos=None, errors=None)


def test_headers_and_qsos():
    imput = Position('<PROGRAMID:9>ADIF2JSON\n<PROGRAMVERSION:5>0.0.1\n<EOH>\n<QSO_DATE:8>20180101\n<EOR>\n')
    res = _read_fields(imput)

    assert res == Adif(headers=Record({'PROGRAMID': 'ADIF2JSON', 'PROGRAMVERSION': '0.0.1'}), qsos=[Record({'QSO_DATE': '20180101'})], errors=None)
