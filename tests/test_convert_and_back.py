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
    js = "".join(to_json_lines(adif))
    print(js)
    res = to_adif(js).strip()
    print(res)

    assert res == adif[0]


def test_simple_qso_with_header():
    adif = ["<myheader:1>1<EOH><call:6>EA4HFF<EOR>"]
    json_lines = "".join(to_json_lines(adif))
    print(json_lines)
    res = from_json_lines(json_lines).strip()

    assert res == adif[0]


def test_multiple_header():
    adif = ["<myheader:1>1<myheader2:2>12<EOH><call:6>EA4HFF<EOR>"]
    res = from_json_lines("".join(to_json_lines(adif))).strip()

    assert res == adif[0]


def test_multiple_qso():
    adif = ["<call:6>EA4HFF<EOR><call:5>EA4AW<EOR>"]
    res = from_json_lines("".join(to_json_lines(adif))).strip()

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
    res = from_json_lines("".join(json_res)).strip()

    print(json_res)
    print("====================")
    print(res)

    assert _string_similar(res, "".join(adif))
