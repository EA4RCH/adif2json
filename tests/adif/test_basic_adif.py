from adif2json.adif import to_dict


def test_empty():
    imput = ""
    res = to_dict(imput)

    assert res == {}, "Empty string should return empty dict"


def test_simplest_empty_headers():
    imput = "<EOH>\n"
    res = to_dict(imput)

    assert res == {"headers": None}, "Empty headers with EOH should return headers=None"


def test_simplest_empty_headers_with_space():
    imput = "<EOH>         \n"
    res = to_dict(imput)

    assert res is not None, "Empty headers with EOH should return something"
    assert "headers" in res, "Empty headers with EOH should return headers property"
    assert res == {"headers": None}, "Empty headers with EOH should return headers=None"


def test_one_header():
    imput = "<myheader:1>1\n<EOH>\n"
    res = to_dict(imput)

    assert res is not None, "One header should return something"
    assert "headers" in res, "One header should return headers"
    header = res["headers"]
    assert "fields" in header, "One header should return header with fields"
    fields = header["fields"]
    assert "myheader" in fields, "One header should return field named myheader"
    assert fields["myheader"] == "1", "One header should return field with value 1"


def test_multiple_headers():
    imput = "<myheader:1>1\n<myheader2:2>12\n<EOH>\n"
    res = to_dict(imput)

    assert res is not None, "Multiple headers should return something"
    assert "headers" in res, "Multiple headers should return headers"
    header = res["headers"]
    assert "fields" in header, "Multiple headers should return header with fields"
    fields = header["fields"]
    assert (
        fields["myheader"] == "1"
    ), "Multiple headers should return header with value 1"
    assert (
        fields["myheader2"] == "12"
    ), "Multiple headers should return header with value 12"


def test_first_header_bad_then_right():
    imput = "<bad:x>1\n<myheader:1>1\n<EOH>\n"
    res = to_dict(imput)

    assert res is not None, "First header bad then right should return something"
    assert "headers" in res, "First header bad then right should return headers"
    assert (
        len(res["headers"]) == 1
    ), "First header bad then right should return one header"
    header = res["headers"]
    assert (
        "fields" in header
    ), "First header bad then right should return header with fields"
    fields = header["fields"]
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
    res = to_dict(imput)

    assert res["headers"] is None, "Headers expected to be None"
    assert len(res["errors"]) == 2, "Two errors expected"
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
    res = to_dict(imput)

    assert res is not None, "Last header bad should return something"
    assert "headers" in res, "Last header bad should return headers"
    header = res["headers"]
    assert "fields" in header, "Last header bad should return header with fields"
    fields = header["fields"]
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
    res = to_dict(imput)

    assert res is not None, "One qso should return something"
    assert "qsos" in res, "One qso should return qsos"
    assert len(res["qsos"]) == 1, "One qso should return one qso"
    qso = res["qsos"][0]
    assert "fields" in qso, "One qso should return qso with fields"
    fields = qso["fields"]
    assert "call" in fields, "One qso should return field named call"
    assert fields["call"] == "EA4HFF", "One qso should return call EA4HFF"


def test_several_qsos():
    imput = "<call:6>EA4HFF<EOR><call:5>EA4AW<EOR><call:4>EC5A<EOR>"
    res = to_dict(imput)

    assert res is not None, "Several qsos should return something"
    assert "qsos" in res, "Several qsos should return qsos"
    assert len(res["qsos"]) == 3, "Several qsos should return three qsos"
    qso = res["qsos"][0]
    assert "fields" in qso, "Several qsos should return qso with fields"
    fields = qso["fields"]
    assert "call" in fields, "Several qsos should return field named call"
    assert fields["call"] == "EA4HFF", "Several qsos should return call EA4HFF"
    qso = res["qsos"][1]
    assert "fields" in qso, "Several qsos should return qso with fields"
    fields = qso["fields"]
    assert "call" in fields, "Several qsos should return field named call"
    assert fields["call"] == "EA4AW", "Several qsos should return call EA4AW"
    qso = res["qsos"][2]
    assert "fields" in qso, "Several qsos should return qso with fields"
    fields = qso["fields"]
    assert "call" in fields, "Several qsos should return field named call"
    assert fields["call"] == "EC5A", "Several qsos should return call EC5A"


def test_headers_and_qsos():
    imput = """
    <program:9>aidf2json<EOH>
    <call:6>EA4HFF<EOR>
    <call:5>EA4AW<EOR>
    <call:4>EC5A<EOR>
    """
    res = to_dict(imput)

    assert res is not None, "Headers and qsos should return something"
    assert "headers" in res, "Headers and qsos should return headers"
    header = res["headers"]
    assert "fields" in header, "Headers and qsos should return header with fields"
    fields = header["fields"]
    assert "program" in fields, "Headers and qsos should return field named program"
    assert (
        fields["program"] == "aidf2json"
    ), "Headers and qsos should return program aidf2json"
    assert "qsos" in res, "Headers and qsos should return qsos"
    assert len(res["qsos"]) == 3, "Headers and qsos should return three qsos"
    qso = res["qsos"][0]
    assert "fields" in qso, "Several qsos should return qso with fields"
    fields = qso["fields"]
    assert "call" in fields, "Several qsos should return field named call"
    assert fields["call"] == "EA4HFF", "Several qsos should return call EA4HFF"
    qso = res["qsos"][1]
    assert "fields" in qso, "Several qsos should return qso with fields"
    fields = qso["fields"]
    assert "call" in fields, "Several qsos should return field named call"
    assert fields["call"] == "EA4AW", "Several qsos should return call EA4AW"
    qso = res["qsos"][2]
    assert "fields" in qso, "Several qsos should return qso with fields"
    fields = qso["fields"]
    assert "call" in fields, "Several qsos should return field named call"
    assert fields["call"] == "EC5A", "Several qsos should return call EC5A"


def test_truncated_at_first():
    imput = """
    <call:6>EA4HFF"""
    res = to_dict(imput)

    assert res is not None, "Truncated at first should return something"
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
    res = to_dict(imput)

    assert res is not None, "Truncated qsos should return something"
    assert "headers" in res, "Truncated qsos should return headers"
    header = res["headers"]
    assert "fields" in header, "Truncated qsos should return header with fields"
    fields = header["fields"]
    assert "program" in fields, "Truncated qsos should return field named program"
    assert (
        fields["program"] == "aidf2json"
    ), "Truncated qsos should return program aidf2json"
    assert "qsos" in res, "Truncated qsos should return qsos"
    assert len(res["qsos"]) == 3, "Truncated qsos should return three qsos"
    qso = res["qsos"][0]
    assert "fields" in qso, "Truncated qsos should return qso with fields"
    fields = qso["fields"]
    assert "call" in fields, "Truncated qsos should return field named call"
    assert fields["call"] == "EA4HFF", "Truncated qsos should return call EA4HFF"
    qso = res["qsos"][1]
    assert "fields" in qso, "Truncated qsos should return qso with fields"
    fields = qso["fields"]
    assert "call" in fields, "Truncated qsos should return field named call"
    assert fields["call"] == "EA4AW", "Truncated qsos should return call EA4AW"
    qso = res["qsos"][2]
    assert "fields" in qso, "Truncated qsos should return qso with fields"
    fields = qso["fields"]
    assert "call" in fields, "Truncated qsos should return field named call"
    assert fields["call"] == "EC5A", "Truncated qsos should return call EC5A"
    assert "errors" in res, "Truncated qsos should return errors"
    assert len(res["errors"]) == 1, "Truncated qsos should return one error"
    error = res["errors"][0]
    assert "reason" in error, "Truncated qsos should return error with reason"
    assert (
        error["reason"] == "TRUNCATED_FILE"
    ), "Truncated qsos should return error TRUNCATED_FILE"
    assert "line" in error, "Truncated qsos should return error with line"
    assert error["line"] == 5, "Truncated qsos should return error in line 5"
    assert "column" in error, "Truncated qsos should return error with column"
    assert error["column"] == 16, "Truncated qsos should return error in column 16"
