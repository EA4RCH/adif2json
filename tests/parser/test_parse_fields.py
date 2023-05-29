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
    s = par.stream_character("<CALL:4>W1AW")
    res = list(par.parse_fields(s))

    print(res)
    assert len(res) == 1
    assert res[0] == {"fields": {"CALL": "W1AW"}}


# FIXME: continue here
