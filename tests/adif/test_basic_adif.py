from adif2json.adif import to_dict


def test_empty():
    imput = [""]
    res = list(to_dict(imput))

    assert len(res) == 0, "Empty string should return empty list"


def test_simplest_empty_headers():
    imput = ["<EOH>\n"]
    res_l = list(to_dict(imput))

    assert len(res_l) == 1, "Empty headers should return one record"
    res = res_l[0]

    expected = {
        "_meta": {
            "type": "headers"
        }
    }

    assert res == expected


def test_simplest_empty_headers_with_space():
    imput = ["<EOH>         \n"]
    res_l = list(to_dict(imput))

    assert len(res_l) == 1, "Empty headers should return one record"
    res = res_l[0]

    expected = {
        "_meta": {
            "type": "headers"
        }
    }

    assert res == expected


def test_one_header():
    imput = ["<myheader:1>1\n<EOH>\n"]
    res_l = list(to_dict(imput))

    assert len(res_l) == 1, "One header should return one record"
    res = res_l[0]

    expected = {
        "myheader": "1",
        "_meta": {
            "type": "headers"
        }
    }

    assert res == expected


def test_multiple_headers():
    imput = ["<myheader:1>1\n<myheader2:2>12\n<EOH>\n"]
    res_l = list(to_dict(imput))

    assert len(res_l) == 1, "One header should return one record"
    res = res_l[0]

    expected = {
        "myheader": "1",
        "myheader2": "12",
        "_meta": {
            "type": "headers"
        }
    }

    assert res == expected


def test_first_header_bad_then_right():
    imput = ["<bad:x>1\n<myheader:1>1\n<EOH>\n"]
    res_l = list(to_dict(imput))

    assert len(res_l) == 1, "One header should return one record"
    res = res_l[0]

    expected = {
        "myheader": "1",
        "_meta": {
            "type": "headers",
            "errors": [
                {"msg": "Size must be a non decimal number", "part": "bad:x"}
            ]
        }
    }

    assert res == expected


def test_all_bad_headers():
    imput = ["<bad:x>1\n<bad2:x>12\n<EOH>\n"]
    res_l = list(to_dict(imput))

    res = res_l[0]

    expected = {
        "_meta": {
            "type": "headers",
            "errors": [
                {"msg": "Size must be a non decimal number", "part": "bad:x"},
                {"msg": "Size must be a non decimal number", "part": "bad2:x"}
            ]
        }
    }

    assert res == expected


def test_last_bad_header():
    imput = ["<myheader:1>1\n<bad:x>12\n<EOH>\n"]
    res_l = list(to_dict(imput))

    res = res_l[0]

    expected = {
        "myheader": "1",
        "_meta": {
            "type": "headers",
            "errors": [
                {"msg": "Size must be a non decimal number", "part": "bad:x"}
            ]
        }
    }

    assert res == expected


def test_one_qso():
    imput = ["<call:6>EA4HFF<EOR>"]
    res_l = list(to_dict(imput))

    res = res_l[0]

    expected = {
        "call": "EA4HFF",
        "_meta": {
            "type": "qso",
        }
    }


def test_several_qsos():
    imput = ["<call:6>EA4HFF<EOR><call:5>EA4AW<EOR><call:4>EC5A<EOR>"]
    res_l = list(to_dict(imput))

    expected_l = [
        {
            "call": "EA4HFF",
            "_meta": {
                "type": "qso",
            }
        },
        {
            "call": "EA4AW",
            "_meta": {
                "type": "qso",
            }
        },
        {
            "call": "EC5A",
            "_meta": {
                "type": "qso",
            }
        }
    ]

    assert res_l == expected_l


def test_headers_and_qsos():
    imput = [
        "<program:9>aidf2json<EOH>",
        "<call:6>EA4HFF<EOR>",
        "<call:5>EA4AW<EOR>",
        "<call:4>EC5A<EOR>",
    ]
    res_l = list(to_dict(imput))

    expected_l = [
        {
            "program": "aidf2json",
            "_meta": {
                "type": "headers",
            }
        },
        {
            "call": "EA4HFF",
            "_meta": {
                "type": "qso",
            }
        },
        {
            "call": "EA4AW",
            "_meta": {
                "type": "qso",
            }
        },
        {
            "call": "EC5A",
            "_meta": {
                "type": "qso",
            }
        }
    ]

    assert res_l == expected_l


def test_truncated_at_first():
    imput = [
        "",
        "<call:6>EA4HFF",
    ]
    res_l = list(to_dict(imput))

    res = res_l[0]

    expected = {
        "call": "EA4HFF",
        "_meta": {
            "errors": [
                {
                    "msg": "Truncated Record",
                    "part": ""
                }
            ],
            "type": "qso"
        }
    }

    assert res == expected


def test_truncated_qsos():
    imput = [
        "<program:9>aidf2json<EOH>",
        "<call:6>EA4HFF<EOR>",
        "<call:5>EA4AW<EOR>",
        "<call:4>EC5A",
    ]
    res_l = list(to_dict(imput))

    expected_l = [
        {
            "program": "aidf2json",
            "_meta": {
                "type": "headers",
            }
        },
        {
            "call": "EA4HFF",
            "_meta": {
                "type": "qso",
            }
        },
        {
            "call": "EA4AW",
            "_meta": {
                "type": "qso",
            }
        },
        {
            "call": "EC5A",
            "_meta": {
                "type": "qso",
                "errors": [
                    {
                        "msg": "Truncated Record",
                        "part": ""
                    }
                ]
            }
        }
    ]

    assert res_l == expected_l
