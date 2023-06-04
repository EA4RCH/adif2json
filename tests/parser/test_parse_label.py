import adif2json.parser as par


def test_eoh():
    res = par._parse_label(par.Eoh(), "")

    assert res == (par.Eoh(), "")


def test_eor():
    res = par._parse_label(par.Eor(), "")

    assert res == (par.Eor(), "")


def test_simple_field():
    res = par._parse_label("TEST:5", "12345")

    assert res == (("TEST", 5, None), "12345")


def test_empty_label():
    res = par._parse_label("", "12345")
    assert res == (par.FormatError("Empty label", ""), "12345")


def test_float_size():
    res = par._parse_label("TEST:5.5", "12345")
    assert res == (
        par.FormatError("Size must be a non decimal number", "TEST:5.5"),
        "12345",
    )


def test_char_size():
    res = par._parse_label("TEST:5a", "12345")
    assert res == (
        par.FormatError("Size must be a non decimal number", "TEST:5a"),
        "12345",
    )


def test_tipe():
    res = par._parse_label("TEST:5:V", "12345")
    assert res == (("TEST", 5, "V"), "12345")


def test_tipe_too_long():
    res = par._parse_label("TEST:5:VV", "12345")
    assert res == (
        par.FormatError("Type must be one Character", "TEST:5:VV"),
        "12345",
    )
