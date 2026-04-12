from adif2json.adif import to_dict


def test_report_invalid_label():
    imput = ["<call:6>EA4HFF<EOR><call:5>EA4AW<EOR><:4>EC5A<EOR>"]

    res_l = list(to_dict(imput))

    expected_l = [
        {
            "call": "EA4HFF",
            "_type": "qso",
        },
        {
            "call": "EA4AW",
            "_type": "qso",
        },
        {
            "_type": "qso",
            "_errors": [
                {
                    "msg": "Empty label",
                    "part": ":4",
                }
            ],
        },
    ]

    assert res_l == expected_l


def test_report_invalid_size():
    imput = ["<call:6>EA4HFF<EOR><call:x>EA4AW<EOR><call:4>EC5A<EOR>"]

    res_l = list(to_dict(imput))

    expected_l = [
        {
            "call": "EA4HFF",
            "_type": "qso",
        },
        {
            "_type": "qso",
            "_errors": [
                {
                    "msg": "Size must be a non decimal number",
                    "part": "call:x",
                }
            ],
        },
        {
            "call": "EC5A",
            "_type": "qso",
        },
    ]

    assert res_l == expected_l


def test_report_invalid_type():
    imput = ["<call:6:8>EA4HFF<EOR><call:5>EA4AW<EOR><call:4>EC5A<EOR>"]

    res_l = list(to_dict(imput))

    expected_l = [
        {
            "_type": "qso",
            "_errors": [
                {
                    "msg": "Type must be one Character",
                    "part": "call:6:8",
                }
            ],
        },
        {
            "call": "EA4AW",
            "_type": "qso",
        },
        {
            "call": "EC5A",
            "_type": "qso",
        },
    ]

    assert res_l == expected_l


def test_report_exceedent_value():
    imput = ["<call:6>EA4HFF tha best<EOR><call:5>EA4AW<EOR><call:4>EC5A<EOR>"]
    res_l = list(to_dict(imput))

    expected_l = [
        {
            "call": "EA4HFF",
            "_type": "qso",
            "_errors": [
                {
                    "msg": "Exeedent value",
                    "part": " tha best",
                }
            ],
        },
        {
            "call": "EA4AW",
            "_type": "qso",
        },
        {
            "call": "EC5A",
            "_type": "qso",
        },
    ]

    assert res_l == expected_l


def test_report_invalid_label_multifield():
    imput = [
        "<call:6>EA4HFF<band:3>40m<EOR>",
        "<call:5>EA4AW<band:3>40m<EOR>",
        "<:4>EC5A<band:3>40m<EOR>",
    ]

    res_l = list(to_dict(imput))

    expected_l = [
        {
            "call": "EA4HFF",
            "band": "40m",
            "_type": "qso",
        },
        {
            "call": "EA4AW",
            "band": "40m",
            "_type": "qso",
        },
        {
            "band": "40m",
            "_type": "qso",
            "_errors": [
                {
                    "msg": "Empty label",
                    "part": ":4",
                }
            ],
        },
    ]

    assert res_l == expected_l


def test_report_invalid_size_multifield():
    imput = [
        "<call:6>EA4HFF<band:3>40m<EOR>",
        "<call:x>EA4AW<band:3>40m<EOR>",
        "<call:4>EC5A<band:3>40m<EOR>",
    ]

    res_l = list(to_dict(imput))

    expected_l = [
        {
            "call": "EA4HFF",
            "band": "40m",
            "_type": "qso",
        },
        {
            "band": "40m",
            "_type": "qso",
            "_errors": [
                {
                    "msg": "Size must be a non decimal number",
                    "part": "call:x",
                }
            ],
        },
        {
            "call": "EC5A",
            "band": "40m",
            "_type": "qso",
        },
    ]

    assert res_l == expected_l


def test_report_invalid_type_multifield():
    imput = [
        "<call:6:8>EA4HFF<band:3>40m<EOR>",
        "<call:5>EA4AW<band:3>40m<EOR>",
        "<call:4>EC5A<band:3>40m<EOR>",
    ]

    res_l = list(to_dict(imput))

    expected_l = [
        {
            "band": "40m",
            "_type": "qso",
            "_errors": [
                {
                    "msg": "Type must be one Character",
                    "part": "call:6:8",
                }
            ],
        },
        {
            "call": "EA4AW",
            "band": "40m",
            "_type": "qso",
        },
        {
            "call": "EC5A",
            "band": "40m",
            "_type": "qso",
        },
    ]

    assert res_l == expected_l


def test_report_exceedent_value_multifield():
    imput = [
        "<call:6>EA4HFF tha best<band:3>40m<EOR>",
        "<call:5>EA4AW<band:3>40m<EOR>",
        "<call:4>EC5A<band:3>40m<EOR>",
    ]

    res_l = list(to_dict(imput))

    expected_l = [
        {
            "call": "EA4HFF",
            "band": "40m",
            "_type": "qso",
            "_errors": [
                {
                    "msg": "Exeedent value",
                    "part": " tha best",
                }
            ],
        },
        {
            "call": "EA4AW",
            "band": "40m",
            "_type": "qso",
        },
        {
            "call": "EC5A",
            "band": "40m",
            "_type": "qso",
        },
    ]

    assert res_l == expected_l
