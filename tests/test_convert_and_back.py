from adif2json.adif import to_json
from adif2json.json import to_adif


def test_empty():
    adif = ''
    res = to_adif(to_json(adif))

    assert res == adif


def test_simple_qso():
    adif = '<call:6>EA4HFF<EOR>'
    res = to_adif(to_json(adif)).strip()

    assert res == adif


def test_simple_qso_with_header():
    adif = '<myheader:1>1<EOH><call:6>EA4HFF<EOR>'
    res = to_adif(to_json(adif)).strip()

    assert res == adif


def test_multiple_header():
    adif = '<myheader:1>1<myheader2:2>12<EOH><call:6>EA4HFF<EOR>'
    res = to_adif(to_json(adif)).strip()

    assert res == adif


def test_multiple_qso():
    adif = '<call:6>EA4HFF<EOR><call:5>EA4AW<EOR>'
    res = to_adif(to_json(adif)).strip()

    assert res == adif


def test_multiple_qso_with_multiple_header():
    adif = '<myheader:1>1<myheader2:2>12<EOH><call:6>EA4HFF<EOR><call:5>EA4AW<EOR>'
    res = to_adif(to_json(adif)).strip()

    assert res == adif
