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
