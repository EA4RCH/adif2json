import adif2json.parser as par


def test_empty_string():
    s = par.stream_character("")
    res = list(par.parse_fields(s))

    assert len(res) == 0


def test_garbage():
    s = par.stream_character(";lhaiopdsaf;a;jlnewo[ivaj;asd'fha")
    res = list(par.parse_fields(s))

    assert len(res) == 0


def test_one_correct_field():
    s = par.stream_character("<CALL:4>EC5A")
    res = list(par.parse_fields(s))

    assert len(res) == 1
    assert res[0] == par.Field("CALL", "EC5A")


def test_headers():
    s = par.stream_character("<PROGRAMID:9>adif2json <EOH> <CALL:4>EC5A<EOR>")
    res = list(par.parse_fields(s))

    assert len(res) == 4
    assert res[0] == par.Field("PROGRAMID", "adif2json")
    assert res[1] == par.Eoh()
    assert res[2] == par.Field("CALL", "EC5A")
    assert res[3] == par.Eor()


def test_compact_fields():
    s = par.stream_character("<CALL:4>EC5A<BAND:3>20M<MODE:3>SSB<EOR>")
    res = list(par.parse_fields(s))

    assert len(res) == 4
    assert res[0] == par.Field("CALL", "EC5A")
    assert res[1] == par.Field("BAND", "20M")
    assert res[2] == par.Field("MODE", "SSB")
    assert res[3] == par.Eor()


def test_invalid_tipe():
    s = par.stream_character("<CALL:4>EC5A<INVALID:3:0>20M<EOR>")
    res = list(par.parse_fields(s))

    assert len(res) == 3
    assert res[0] == par.Field("CALL", "EC5A")
    assert res[1] == par.ParseError(
        "Type must be one Character", [par.Character("0", 1, 24)]
    )
    assert res[2] == par.Eor()


def test_invalid_size():
    s = par.stream_character("<CALL:Z>EC5A<EOR>")
    res = list(par.parse_fields(s))

    assert len(res) == 2
    assert res[0] == par.ParseError(
        "Size must be a non decimal number", [par.Character("Z", 1, 7)]
    )
    assert res[1] == par.Eor()


def test_invalid_label():
    s = par.stream_character("<CALL:4>EC5A<:3>20M<EOR>")
    res = list(par.parse_fields(s))

    assert len(res) == 3
    assert res[0] == par.Field("CALL", "EC5A")
    assert res[1] == par.ParseError(
        "Empty label", [par.Character(":", 1, 14), par.Character("3", 1, 15)]
    )
    assert res[2] == par.Eor()


def test_tructacted_value():
    s = par.stream_character("<CALL:4>EC5A<MODE:3>SS<EOR>")
    res = list(par.parse_fields(s))

    assert len(res) == 3
    assert res[0] == par.Field("CALL", "EC5A")
    assert res[1] == par.ParseError(
        "Size is bigger than value",
        [par.Character("S", 1, 21), par.Character("S", 1, 22)],
    )
    assert res[2] == par.Eor()


def test_exceedent_value_first():
    s = par.stream_character("<CALL:4>EC5A tha best!!<MODE:3>SSB<EOR>")
    res = list(par.parse_fields(s))

    assert len(res) == 4
    assert res[0] == par.ParseError(
        "Excedeent value", list(par.stream_character(" tha best!!", c=12))
    )
    assert res[1] == par.Field("CALL", "EC5A")
    assert res[2] == par.Field("MODE", "SSB")
    assert res[3] == par.Eor()
