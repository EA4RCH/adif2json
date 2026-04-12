import json

from adif2json.adif import to_json_lines
from adif2json.json import from_json_lines, to_adif


def _string_similar(s1, s2):
    a = "".join(s1.split())
    b = "".join(s2.split())
    return a == b


def test_empty():
    adif = [""]
    res_js = list(to_json_lines(adif))
    js = "".join(res_js)
    res = to_adif(js)

    assert res == adif[0]


def test_simple_qso():
    adif = ["<call:6>EA4HFF<EOR>"]
    json_lines = list(to_json_lines(adif))
    flat = json.loads(json_lines[0])

    assert flat == {
        "call": "EA4HFF",
        "_type": "qso",
    }

    res = to_adif("".join(json_lines)).strip()

    assert res == adif[0]


def test_simple_qso_with_header():
    adif = ["<myheader:1>1<EOH><call:6>EA4HFF<EOR>"]
    json_lines = list(to_json_lines(adif))
    header = json.loads(json_lines[0])
    qso = json.loads(json_lines[1])

    assert header == {
        "myheader": "1",
        "_type": "headers",
    }
    assert qso == {
        "call": "EA4HFF",
        "_type": "qso",
    }

    res = from_json_lines("".join(json_lines)).strip()

    assert res == adif[0]


def test_multiple_header():
    adif = ["<myheader:1>1<myheader2:2>12<EOH><call:6>EA4HFF<EOR>"]
    json_lines = list(to_json_lines(adif))
    header = json.loads(json_lines[0])

    assert header == {
        "myheader": "1",
        "myheader2": "12",
        "_type": "headers",
    }

    res = from_json_lines("".join(json_lines)).strip()

    assert res == adif[0]


def test_multiple_qso():
    adif = ["<call:6>EA4HFF<EOR><call:5>EA4AW<EOR>"]
    json_lines = list(to_json_lines(adif))

    assert json.loads(json_lines[0]) == {
        "call": "EA4HFF",
        "_type": "qso",
    }
    assert json.loads(json_lines[1]) == {
        "call": "EA4AW",
        "_type": "qso",
    }

    res = from_json_lines("".join(json_lines)).strip()

    assert res == adif[0]


def test_multiple_qso_with_multiple_header():
    adif = [
        "<myheader:1>1<myheader2:2>12<EOH>",
        "<call:6>EA4HFF<EOR><call:5>EA4AW<EOR>",
    ]
    res = from_json_lines("".join(to_json_lines(adif))).strip()

    assert _string_similar(res, "".join(adif))


def test_multiple_qso_with_multiple_header_and_types():
    adif = [
        "<myheader:1:N>1<myheader2:2>12<EOH>",
        "<call:6:S>EA4HFF<EOR><call:5>EA4AW<EOR>",
    ]
    json_res = list(to_json_lines(adif))
    header = json.loads(json_res[0])
    qso = json.loads(json_res[1])
    res = from_json_lines("".join(json_res)).strip()

    assert header == {
        "myheader": "1",
        "myheader2": "12",
        "_type": "headers",
        "_types": {
            "myheader": "N",
        },
    }
    assert qso == {
        "call": "EA4HFF",
        "_type": "qso",
        "_types": {
            "call": "S",
        },
    }
    assert _string_similar(res, "".join(adif))
