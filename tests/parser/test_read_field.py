import adif2json.parser as par


def test_expected_eoh():
    res = list(par._read_field(par.Eoh(), ""))

    assert res == [par.Eoh()]


def test_expected_eor():
    res = list(par._read_field(par.Eor(), ""))

    assert res == [par.Eor()]


def test_expected_error():
    res = list(par._read_field(par.FormatError("Error", ""), ""))

    assert res == [par.FormatError("Error", "")]


def test_expected_field():
    res = list(par._read_field(("TEST", 5, None), "12345"))

    assert res == [par.Field("TEST", "12345", None)]


def test_truncated_field():
    res = list(par._read_field(("TEST", 5, None), "1234"))

    assert res == [
        par.FormatError("Truncated value", "1234"),
        par.Field("TEST", "1234", None),
    ]


def test_exeedent_field():
    res = list(par._read_field(("TEST", 5, None), "123456"))

    assert res == [
        par.FormatError("Exeedent value", "6"),
        par.Field("TEST", "12345", None),
    ]
