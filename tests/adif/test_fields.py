from adif2json.adif import _read_fields, Adif, Record
from adif2json.parser import Position


def test_empty():
    imput = Position('')
    res = _read_fields(imput)

    assert res == Adif()


def test_qsos():
    imput = Position('<EOH>\n<QSO_DATE:8>20180101\n<EOR>\n')
    res = _read_fields(imput)

    assert res == Adif(headers=None, qsos=[Record({'QSO_DATE': '20180101'})])
