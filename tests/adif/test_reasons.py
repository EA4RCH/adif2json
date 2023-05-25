from adif2json.adif import to_dict


def test_report_invalid_label():
    imput = "<call:6>EA4HFF<EOR><call:5>EA4AW<EOR><:4>EC5A<EOR>"

    res_l = list(to_dict(imput))

    assert len(res_l) == 3
    res = res_l[0]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EA4HFF"}
    assert res["errors"] is None
    res = res_l[1]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EA4AW"}
    assert res["errors"] is None
    res = res_l[2]
    assert res["type"] == "qso"
    assert res["fields"] == {}
    assert res["errors"] is not None
    assert len(res["errors"]) == 1
    error = res["errors"][0]
    assert error["reason"] == "INVALID_LABEL"
    assert error["line"] == 1
    assert error["column"] == 39


def test_report_invalid_size():
    imput = "<call:6>EA4HFF<EOR><call:x>EA4AW<EOR><call:4>EC5A<EOR>"

    res_l = list(to_dict(imput))

    assert len(res_l) == 3
    res = res_l[0]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EA4HFF"}
    assert res["errors"] is None
    res = res_l[1]
    assert res["type"] == "qso"
    assert res["fields"] == {}
    assert res["errors"] is not None
    assert len(res["errors"]) == 1
    error = res["errors"][0]
    assert error["reason"] == "INVALID_SIZE"
    assert error["start_line"] == 1
    assert error["start_column"] == 26
    assert error["end_line"] == 1
    assert error["end_column"] == 26
    res = res_l[2]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EC5A"}
    assert res["errors"] is None


def test_report_invalid_type():
    imput = "<call:6:8>EA4HFF<EOR><call:5>EA4AW<EOR><call:4>EC5A<EOR>"

    res_l = list(to_dict(imput))

    assert len(res_l) == 3
    res = res_l[0]
    assert res["type"] == "qso"
    assert res["fields"] == {}
    assert res["errors"] is not None
    assert len(res["errors"]) == 1
    error = res["errors"][0]
    assert error["reason"] == "INVALID_TIPE"
    assert error["line"] == 1
    assert error["column"] == 9
    res = res_l[1]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EA4AW"}
    assert res["errors"] is None
    res = res_l[2]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EC5A"}
    assert res["errors"] is None


def test_report_exceedent_value():
    imput = "<call:6>EA4HFF tha best<EOR><call:5>EA4AW<EOR><call:4>EC5A<EOR>"
    res_l = list(to_dict(imput))

    assert len(res_l) == 3
    res = res_l[0]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EA4HFF"}
    assert len(res["errors"]) == 1
    error = res["errors"][0]
    assert error["reason"] == "EXCEEDENT_VALUE"
    assert error["start_line"] == 1
    assert error["start_column"] == 15
    assert error["end_line"] == 1
    assert error["end_column"] == 23
    res = res_l[1]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EA4AW"}
    assert res["errors"] is None
    res = res_l[2]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EC5A"}
    assert res["errors"] is None


def test_report_invalid_label_multifield():
    imput = """
    <call:6>EA4HFF<band:3>40m<EOR>
    <call:5>EA4AW<band:3>40m<EOR>
    <:4>EC5A<band:3>40m<EOR>
    """

    res = to_dict(imput)

    assert res is not None, "dict expected"
    assert "qsos" in res, "qsos expected"
    qsos = res["qsos"]
    assert len(qsos) == 3, "3 qsos expected"
    qso = qsos[0]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "call" in fields, "call expected"
    assert fields["call"] == "EA4HFF", "EA4HFF expected"
    assert "band" in fields, "band expected"
    assert fields["band"] == "40m", "40m expected"
    qso = qsos[1]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "call" in fields, "call expected"
    assert fields["call"] == "EA4AW", "EA4AW expected"
    assert "band" in fields, "band expected"
    assert fields["band"] == "40m", "40m expected"
    qso = qsos[2]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "band" in fields, "band expected"
    assert fields["band"] == "40m", "40m expected"
    assert "errors" in res, "errors expected"
    errors = res["errors"]
    assert len(errors) == 1, "1 error expected"
    error = errors[0]
    assert "reason" in error, "reason expected"
    assert error["reason"] == "INVALID_LABEL", "INVALID_LABEL expected"
    assert "line" in error, "line expected"
    assert error["line"] == 4, "line 4 expected"
    assert "column" in error, "column expected"
    assert error["column"] == 6, "column 6 expected"


def test_report_invalid_size_multifield():
    imput = """
    <call:6>EA4HFF<band:3>40m<EOR>
    <call:x>EA4AW<band:3>40m<EOR>
    <call:4>EC5A<band:3>40m<EOR>
    """

    res = to_dict(imput)

    assert res is not None, "dict expected"
    assert "qsos" in res, "qsos expected"
    qsos = res["qsos"]
    assert len(qsos) == 3, "3 qsos expected"
    qso = qsos[0]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "call" in fields, "call expected"
    assert fields["call"] == "EA4HFF", "EA4HFF expected"
    assert "band" in fields, "band expected"
    assert fields["band"] == "40m", "40m expected"
    qso = qsos[1]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "band" in fields, "band expected"
    assert fields["band"] == "40m", "40m expected"
    qso = qsos[2]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "call" in fields, "call expected"
    assert fields["call"] == "EC5A", "EC5A expected"
    assert "band" in fields, "band expected"
    assert fields["band"] == "40m", "40m expected"
    assert "errors" in res, "errors expected"
    errors = res["errors"]
    assert len(errors) == 1, "1 error expected"
    error = errors[0]
    assert "reason" in error, "reason expected"
    assert error["reason"] == "INVALID_SIZE", "INVALID_SIZE expected"
    assert "start_line" in error, "start_line expected"
    assert error["start_line"] == 3, "start_line 3 expected"
    assert "start_column" in error, "start_column expected"
    assert error["start_column"] == 11, "start_column 11 expected"
    assert "end_line" in error, "end_line expected"
    assert error["end_line"] == 3, "end_line 3 expected"
    assert "end_column" in error, "end_column expected"
    assert error["end_column"] == 11, "end_column 11 expected"


def test_report_invalid_type_multifield():
    imput = """
    <call:6:8>EA4HFF<band:3>40m<EOR>
    <call:5>EA4AW<band:3>40m<EOR>
    <call:4>EC5A<band:3>40m<EOR>
    """

    res = to_dict(imput)

    assert res is not None, "dict expected"
    assert "qsos" in res, "qsos expected"
    qsos = res["qsos"]
    assert len(qsos) == 3, "3 qsos expected"
    qso = qsos[0]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "band" in fields, "band expected"
    assert fields["band"] == "40m", "40m expected"
    qso = qsos[1]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "call" in fields, "call expected"
    assert fields["call"] == "EA4AW", "EA4AW expected"
    assert "band" in fields, "band expected"
    assert fields["band"] == "40m", "40m expected"
    qso = qsos[2]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "band" in fields, "band expected"
    assert fields["band"] == "40m", "40m expected"
    assert "errors" in res, "errors expected"
    errors = res["errors"]
    assert len(errors) == 1, "1 error expected"
    error = errors[0]
    assert "reason" in error, "reason expected"
    assert error["reason"] == "INVALID_TIPE", "INVALID_TIPE expected"
    assert "line" in error, "start_line expected"
    assert error["line"] == 2, "start_line 2 expected"
    assert "column" in error, "start_column expected"
    assert error["column"] == 13, "start_column 13 expected"


def test_report_exceedent_value_multifield():
    imput = """
    <call:6>EA4HFF tha best<band:3>40m<EOR>
    <call:5>EA4AW<band:3>40m<EOR>
    <call:4>EC5A<band:3>40m<EOR>
    """

    res = to_dict(imput)

    assert res is not None, "dict expected"
    assert "qsos" in res, "qsos expected"
    qsos = res["qsos"]
    assert len(qsos) == 3, "3 qsos expected"
    qso = qsos[0]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "band" in fields, "band expected"
    assert fields["band"] == "40m", "40m expected"
    qso = qsos[1]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "call" in fields, "call expected"
    assert fields["call"] == "EA4AW", "EA4AW expected"
    assert "band" in fields, "band expected"
    assert fields["band"] == "40m", "40m expected"
    qso = qsos[2]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "band" in fields, "band expected"
    assert fields["band"] == "40m", "40m expected"
    assert "errors" in res, "errors expected"
    errors = res["errors"]
    assert len(errors) == 1, "1 error expected"
    error = errors[0]
    assert "reason" in error, "reason expected"
    assert error["reason"] == "EXCEEDENT_VALUE", "EXCEEDENT_VALUE expected"
    assert "start_line" in error, "start_line expected"
    assert error["start_line"] == 2, "start_line 2 expected"
    assert "start_column" in error, "start_column expected"
    assert error["start_column"] == 19, "start_column 19 expected"
    assert "end_line" in error, "end_line expected"
    assert error["end_line"] == 2, "end_line 2 expected"
    assert "end_column" in error, "end_column expected"
    assert error["end_column"] == 27, "end_column 27 expected"
