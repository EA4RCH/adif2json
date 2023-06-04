import adif2json.parser as par


def test_expected_eor():
    res = par._parse_delimiters("EOR", "")

    assert res == (par.Eor(), "")


def test_expected_eoh():
    res = par._parse_delimiters("EOH", "")

    assert res == (par.Eoh(), "")


def test_expected_field():
    res = par._parse_delimiters("CALL", "EA5HUS")

    assert res == ("CALL", "EA5HUS")
