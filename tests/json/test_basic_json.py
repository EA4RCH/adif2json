from adif2json.json import to_adif, from_json_lines


def test_empty():
    res = to_adif("")

    assert res == ""


def test_simple_qso():
    adif = (
            """ { "call": "EA4HFF", "_meta": {"type": "qso"}} """
    )
    expected = "<call:6>EA4HFF<EOR>"
    res = to_adif(adif)

    assert res == expected


def test_simple_qso_with_header():
    adif = """
        {"myheader": "1", "_meta": {"type": "headers"}}
        {"call": "EA4HFF", "_meta": {"type": "qso"}}
    """
    expected = "<myheader:1>1<EOH><call:6>EA4HFF<EOR>"
    res = from_json_lines(adif)

    assert res == expected
