from adif2json.adif import to_dict


def test_empty():
    imput = ""
    res = list(to_dict(imput))

    assert len(res) == 0, "Empty string should return empty list"


def test_simplest_empty_headers():
    imput = "<EOH>\n"
    res_l = list(to_dict(imput))

    assert len(res_l) == 1, "Empty headers should return one record"
    res = res_l[0]
    assert "type" in res, "Empty headers with EOH should return type property"
    assert res["type"] == "headers", "Empty headers with EOH should return type=headers"
    assert "fields" in res, "Empty headers with EOH should return headers property"
    assert res["fields"] == {}, "Empty headers with EOH should return headers={}"
    assert "errors" in res, "Empty headers with EOH should return errors"
    assert res["errors"] is None, "Empty headers with EOH should return errors=None"


def test_simplest_empty_headers_with_space():
    imput = "<EOH>         \n"
    res_l = list(to_dict(imput))

    assert len(res_l) == 1, "Empty headers should return one record"
    res = res_l[0]
    assert "type" in res, "Empty headers with EOH should return type property"
    assert res["type"] == "headers", "Empty headers with EOH should return type=headers"
    assert "fields" in res, "Empty headers with EOH should return headers property"
    assert res["fields"] == {}, "Empty headers with EOH should return headers={}"
    assert "errors" in res, "Empty headers with EOH should return errors"
    assert res["errors"] is None, "Empty headers with EOH should return errors=None"


def test_one_header():
    imput = "<myheader:1>1\n<EOH>\n"
    res_l = list(to_dict(imput))

    assert len(res_l) == 1, "One header should return one record"
    res = res_l[0]
    assert "type" in res, "Empty headers with EOH should return type property"
    assert res["type"] == "headers", "Empty headers with EOH should return type=headers"
    assert "fields" in res, "One header should return header with fields"
    fields = res["fields"]
    assert "myheader" in fields, "One header should return field named myheader"
    assert fields["myheader"] == "1", "One header should return field with value 1"


def test_multiple_headers():
    imput = "<myheader:1>1\n<myheader2:2>12\n<EOH>\n"
    res_l = list(to_dict(imput))

    assert len(res_l) == 1, "One header should return one record"
    res = res_l[0]
    assert "type" in res, "Empty headers with EOH should return type property"
    assert res["type"] == "headers", "Empty headers with EOH should return type=headers"
    assert "fields" in res, "One header should return header with fields"
    fields = res["fields"]
    assert "myheader" in fields, "One header should return field named myheader"
    assert fields["myheader"] == "1", "One header should return field with value 1"
    assert "myheader2" in fields, "One header should return field named myheader2"
    assert fields["myheader2"] == "12", "One header should return field with value 12"


def test_first_header_bad_then_right():
    imput = "<bad:x>1\n<myheader:1>1\n<EOH>\n"
    res_l = list(to_dict(imput))

    assert len(res_l) == 1, "One header should return one record"
    res = res_l[0]
    assert "type" in res, "Empty headers with EOH should return type property"
    assert res["type"] == "headers", "Empty headers with EOH should return type=headers"
    assert "fields" in res, "One header should return header with fields"
    fields = res["fields"]

    assert (
        "myheader" in fields
    ), "First header bad then right should return field named myheader"
    assert (
        fields["myheader"] == "1"
    ), "First header bad then right should return header with value 1"
    assert (
        len(res["errors"]) == 1
    ), "First header bad then right should return one error"
    err = res["errors"][0]
    assert (
        err["reason"] == "INVALID_SIZE"
    ), "First header bad then right should return error INVALID_SIZE"
    assert err["start_line"] == 1
    assert err["start_column"] == 6
    assert err["end_line"] == 1
    assert err["end_column"] == 6


def test_all_bad_headers():
    imput = "<bad:x>1\n<bad2:x>12\n<EOH>\n"
    res_l = list(to_dict(imput))

    res = res_l[0]
    assert "type" in res, "Empty headers with EOH should return type property"
    assert res["type"] == "headers", "Empty headers with EOH should return type=headers"
    assert "fields" in res, "One header should return header with fields"
    assert res["fields"] == {}, "All bad headers should return empty fields"
    assert "errors" in res, "All bad headers should return errors"
    assert len(res["errors"]) == 2, "All bad headers should return two errors"
    err1 = res["errors"][0]
    assert err1["reason"] == "INVALID_SIZE", "First error expected to be INVALID_SIZE"
    assert err1["start_line"] == 1
    assert err1["start_column"] == 6
    assert err1["end_line"] == 1
    assert err1["end_column"] == 6
    err2 = res["errors"][1]
    assert err2["reason"] == "INVALID_SIZE", "Second error expected to be INVALID_SIZE"
    assert err2["start_line"] == 2
    assert err2["start_column"] == 7
    assert err2["end_line"] == 2
    assert err2["end_column"] == 7


def test_last_bad_header():
    imput = "<myheader:1>1\n<bad:x>12\n<EOH>\n"
    res_l = list(to_dict(imput))

    res = res_l[0]
    assert "type" in res, "Empty headers with EOH should return type property"
    assert res["type"] == "headers", "Empty headers with EOH should return type=headers"
    assert "fields" in res, "One header should return header with fields"
    fields = res["fields"]
    assert "myheader" in fields, "Last header bad should return field named myheader"
    assert (
        fields["myheader"] == "1"
    ), "Last header bad should return header with value 1"
    assert "errors" in res, "Last header bad should return errors"
    assert len(res["errors"]) == 1, "Last header bad should return one error"
    err = res["errors"][0]
    assert (
        err["reason"] == "INVALID_SIZE"
    ), "Last header bad should return error INVALID_SIZE"
    assert err["start_line"] == 2
    assert err["start_column"] == 6
    assert err["end_line"] == 2
    assert err["end_column"] == 6


def test_one_qso():
    imput = "<call:6>EA4HFF<EOR>"
    res_l = list(to_dict(imput))

    res = res_l[0]
    assert "type" in res, "One qso should return type property"
    assert res["type"] == "qso", "One qso should return type=qso"
    assert "fields" in res, "One qso should return qso with fields"
    fields = res["fields"]
    assert "call" in fields, "One qso should return field named call"
    assert fields["call"] == "EA4HFF", "One qso should return call EA4HFF"


def test_several_qsos():
    imput = "<call:6>EA4HFF<EOR><call:5>EA4AW<EOR><call:4>EC5A<EOR>"
    res_l = list(to_dict(imput))

    res = res_l[0]
    assert "type" in res, "Several qsos should return type property"
    assert res["type"] == "qso", "Several qsos should return type=qso"
    assert "fields" in res, "Several qsos should return qso with fields"
    fields = res["fields"]
    assert "call" in fields, "Several qsos should return field named call"
    assert fields["call"] == "EA4HFF", "Several qsos should return call EA4HFF"
    res = res_l[1]
    assert "type" in res, "Several qsos should return type property"
    assert res["type"] == "qso", "Several qsos should return type=qso"
    assert "fields" in res, "Several qsos should return qso with fields"
    fields = res["fields"]
    assert "call" in fields, "Several qsos should return field named call"
    assert fields["call"] == "EA4AW", "Several qsos should return call EA4AW"
    res = res_l[2]
    assert "type" in res, "Several qsos should return type property"
    assert res["type"] == "qso", "Several qsos should return type=qso"
    assert "fields" in res, "Several qsos should return qso with fields"
    fields = res["fields"]
    assert "call" in fields, "Several qsos should return field named call"
    assert fields["call"] == "EC5A", "Several qsos should return call EC5A"


def test_headers_and_qsos():
    imput = """
    <program:9>aidf2json<EOH>
    <call:6>EA4HFF<EOR>
    <call:5>EA4AW<EOR>
    <call:4>EC5A<EOR>
    """
    res_l = list(to_dict(imput))

    res = res_l[0]
    assert "type" in res, "Headers and qsos should return type property"
    assert res["type"] == "headers", "Headers and qsos should return type=headers"
    assert "fields" in res, "Headers and qsos should return header with fields"
    fields = res["fields"]
    assert "program" in fields, "Headers and qsos should return field named program"
    assert (
        fields["program"] == "aidf2json"
    ), "Headers and qsos should return program aidf2json"
    res = res_l[1]
    assert "type" in res, "Headers and qsos should return type property"
    assert res["type"] == "qso", "Headers and qsos should return type=qso"
    assert "fields" in res, "Headers and qsos should return qso with fields"
    fields = res["fields"]
    assert "call" in fields, "Headers and qsos should return field named call"
    assert fields["call"] == "EA4HFF", "Headers and qsos should return call EA4HFF"
    res = res_l[2]
    assert "type" in res, "Headers and qsos should return type property"
    assert res["type"] == "qso", "Headers and qsos should return type=qso"
    assert "fields" in res, "Headers and qsos should return qso with fields"
    fields = res["fields"]
    assert "call" in fields, "Headers and qsos should return field named call"
    assert fields["call"] == "EA4AW", "Headers and qsos should return call EA4AW"
    res = res_l[3]
    assert "type" in res, "Headers and qsos should return type property"
    assert res["type"] == "qso", "Headers and qsos should return type=qso"
    assert "fields" in res, "Headers and qsos should return qso with fields"
    fields = res["fields"]
    assert "call" in fields, "Headers and qsos should return field named call"
    assert fields["call"] == "EC5A", "Headers and qsos should return call EC5A"


def test_truncated_at_first():
    imput = """
    <call:6>EA4HFF"""
    res_l = list(to_dict(imput))

    res = res_l[0]
    assert "type" in res, "Truncated at first should return type property"
    assert res["type"] == "qso", "Truncated at first should return type=qso"
    assert "fields" in res, "Truncated at first should return qso with fields"
    fields = res["fields"]
    assert "call" in fields, "Truncated at first should return field named call"
    assert fields["call"] == "EA4HFF", "Truncated at first should return call EA4HFF"
    assert "errors" in res, "Truncated at first should return errors"
    assert len(res["errors"]) == 1, "Truncated at first should return one error"
    err = res["errors"][0]
    assert (
        err["reason"] == "TRUNCATED_FILE"
    ), "Truncated at first should return error TRUNCATED_FILE"
    assert err["line"] == 2, "Truncated at first should return error in line 2"
    assert err["column"] == 18, "Truncated at first should return error in column 18"


def test_truncated_qsos():
    imput = """
    <program:9>aidf2json<EOH>
    <call:6>EA4HFF<EOR>
    <call:5>EA4AW<EOR>
    <call:4>EC5A"""
    res_l = list(to_dict(imput))

    res = res_l[0]
    assert "type" in res, "Truncated qsos should return type property"
    assert res["type"] == "headers", "Truncated qsos should return type=headers"
    assert "fields" in res, "Truncated qsos should return header with fields"
    fields = res["fields"]
    assert "program" in fields, "Truncated qsos should return field named program"
    assert (
        fields["program"] == "aidf2json"
    ), "Truncated qsos should return program aidf2json"
    res = res_l[1]
    assert "type" in res, "Truncated qsos should return type property"
    assert res["type"] == "qso", "Truncated qsos should return type=qso"
    assert "fields" in res, "Truncated qsos should return qso with fields"
    fields = res["fields"]
    assert "call" in fields, "Truncated qsos should return field named call"
    assert fields["call"] == "EA4HFF", "Truncated qsos should return call EA4HFF"
    res = res_l[2]
    assert "type" in res, "Truncated qsos should return type property"
    assert res["type"] == "qso", "Truncated qsos should return type=qso"
    assert "fields" in res, "Truncated qsos should return qso with fields"
    fields = res["fields"]
    assert "call" in fields, "Truncated qsos should return field named call"
    assert fields["call"] == "EA4AW", "Truncated qsos should return call EA4AW"
    res = res_l[3]
    assert "type" in res, "Truncated qsos should return type property"
    assert res["type"] == "qso", "Truncated qsos should return type=qso"
    assert "fields" in res, "Truncated qsos should return qso with fields"
    fields = res["fields"]
    assert "call" in fields, "Truncated qsos should return field named call"
    assert fields["call"] == "EC5A", "Truncated qsos should return call EC5A"
    assert "errors" in res, "Truncated qsos should return errors"
    assert len(res["errors"]) == 1, "Truncated qsos should return one error"
    err = res["errors"][0]
    assert (
        err["reason"] == "TRUNCATED_FILE"
    ), "Truncated qsos should return error TRUNCATED_FILE"
    assert err["line"] == 5, "Truncated qsos should return error in line 5"
    assert err["column"] == 16, "Truncated qsos should return error in column 16"
