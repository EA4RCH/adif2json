import adif2json.parser as par


def test_empty():
    res = par.parse_all("")

    assert res == []


def test_empty_header():
    res = par.parse_all("<EOH>")

    print(res)
    assert res == [par.Eoh()]


def test_one_field():
    res = par.parse_all("<CALL:4>TEST")

    assert res == [
        par.Field("CALL", "TEST"),
    ]


def test_several_fields():
    res = par.parse_all("<CALL:4>TEST<MODE:3>SSB")

    assert res == [
        par.Field("CALL", "TEST"),
        par.Field("MODE", "SSB"),
    ]


def test_several_fields_with_eor():
    res = par.parse_all("<CALL:4>TEST<MODE:3>SSB<EOR>")

    assert res == [
        par.Field("CALL", "TEST"),
        par.Field("MODE", "SSB"),
        par.Eor(),
    ]


def test_several_fields_with_eoh():
    res = par.parse_all("<PROGRAMID:4>TEST <VERSION:5>0.1.0 <EOH>")

    assert res == [
        par.Field("PROGRAMID", "TEST"),
        par.Field("VERSION", "0.1.0"),
        par.Eoh(),
    ]


def test_no_size_label():
    res = par.parse_all("<CALL>Test")

    assert res == [
        par.FormatError("Expect size", "CALL"),
    ]


def test_empty_label():
    res = par.parse_all("<:4>Test")

    assert res == [
        par.FormatError("Empty label", ":4"),
    ]


def test_bad_size():
    res = par.parse_all("<CALL:4a>Test")

    assert res == [
        par.FormatError("Size must be a non decimal number", "CALL:4a"),
    ]


def test_bad_tipe():
    res = par.parse_all("<CALL:4:BAD>Test")

    assert res == [
        par.FormatError("Type must be one Character", "CALL:4:BAD"),
    ]


def test_bad_tipe_2():
    res = par.parse_all("<CALL:4:1>Test")

    assert res == [
        par.FormatError("Type must be one Character", "CALL:4:1"),
    ]


def test_truncated_value():
    res = par.parse_all("<CALL:4>")

    assert res == [
        par.FormatError("Empty value", "('CALL', 4, None)"),
    ]


def test_exeedent_value():
    res = par.parse_all("<CALL:4>TESTE")

    assert res == [
        par.FormatError("Exeedent value", "E"),
        par.Field("CALL", "TEST"),
    ]


def test_truncated_value_2():
    res = par.parse_all("<CALL:4>TE<MODE:3>SSB")

    assert res == [
        par.FormatError("Truncated value", "TE"),
        par.Field("CALL", "TE"),
        par.Field("MODE", "SSB"),
    ]
