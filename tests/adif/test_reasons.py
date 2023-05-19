from adif2json.adif import to_dict


def test_report_invalid_label():
    imput = "<call:6>EA4HFF<EOR><call:5>EA4AW<EOR><:4>EC5A<EOR>"

    res = to_dict(imput)

    assert res is not None, "dict expected"
    assert "qsos" in res, "qsos expected"
    qsos = res["qsos"]
    assert len(qsos) == 2, "2 qsos expected"
    qso = qsos[0]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "call" in fields, "call expected"
    assert fields["call"] == "EA4HFF", "EA4HFF expected"
    qso = qsos[1]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "call" in fields, "call expected"
    assert fields["call"] == "EA4AW", "EA4AW expected"
    assert "errors" in res, "errors expected"
    errors = res["errors"]
    assert len(errors) == 1, "1 error expected"
    error = errors[0]
    assert "reason" in error, "reason expected"
    assert error["reason"] == "INVALID_LABEL", "INVALID_LABEL expected"
    assert "line" in error, "line expected"
    assert error["line"] == 1, "line 1 expected"
    assert "column" in error, "column expected"
    assert error["column"] == 39, "column 39 expected"
    assert "size" in error, "size expected"
    assert error["size"] == 1, "size 1 expected"


def test_report_invalid_size():
    imput = "<call:6>EA4HFF<EOR><call:x>EA4AW<EOR><call:4>EC5A<EOR>"

    res = to_dict(imput)

    assert res is not None, "dict expected"
    assert "qsos" in res, "qsos expected"
    qsos = res["qsos"]
    assert len(qsos) == 2, "2 qsos expected"
    qso = qsos[0]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "call" in fields, "call expected"
    assert fields["call"] == "EA4HFF", "EA4HFF expected"
    qso = qsos[1]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "call" in fields, "call expected"
    assert fields["call"] == "EC5A", "EC5A expected"
    assert "errors" in res, "errors expected"
    errors = res["errors"]
    assert len(errors) == 1, "1 error expected"
    error = errors[0]
    assert "reason" in error, "reason expected"
    assert error["reason"] == "INVALID_SIZE", "INVALID_SIZE expected"
    assert "line" in error, "line expected"
    assert error["line"] == 1, "line 1 expected"
    assert "column" in error, "column expected"
    assert error["column"] == 25, "column 25 expected"
    assert "size" in error, "size expected"
    assert error["size"] == 1, "size 1 expected"


def test_report_invalid_type():
    imput = "<call:6:8>EA4HFF<EOR><call:5>EA4AW<EOR><call:4>EC5A<EOR>"

    res = to_dict(imput)

    assert res is not None, "dict expected"
    assert "qsos" in res, "qsos expected"
    qsos = res["qsos"]
    assert len(qsos) == 2, "2 qsos expected"
    qso = qsos[0]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "call" in fields, "call expected"
    assert fields["call"] == "EA4AW", "EA4AW expected"
    qso = qsos[1]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "call" in fields, "call expected"
    assert fields["call"] == "EC5A", "EC5A expected"
    assert "errors" in res, "errors expected"
    errors = res["errors"]
    assert len(errors) == 1, "1 error expected"
    error = errors[0]
    assert "reason" in error, "reason expected"
    assert error["reason"] == "INVALID_TIPE", "INVALID_TIPE expected"
    assert "line" in error, "line expected"
    assert error["line"] == 1, "line 1 expected"
    assert "column" in error, "column expected"
    assert error["column"] == 8, "column 8 expected"
    assert "size" in error, "size expected"
    assert error["size"] == 1, "size 1 expected"


def test_report_exceedent_value():
    imput = "<call:6>EA4HFF tha best<EOR><call:5>EA4AW<EOR><call:4>EC5A<EOR>"
    res = to_dict(imput)

    assert res is not None, "dict expected"
    assert "qsos" in res, "qsos expected"
    qsos = res["qsos"]
    assert len(qsos) == 2, "2 qsos expected"
    qso = qsos[0]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "call" in fields, "call expected"
    assert fields["call"] == "EA4AW", "EA4AW expected"
    qso = qsos[1]
    assert "fields" in qso, "fields expected"
    fields = qso["fields"]
    assert "call" in fields, "call expected"
    assert fields["call"] == "EC5A", "EC5A expected"
    assert "errors" in res, "errors expected"
    errors = res["errors"]
    assert len(errors) == 1, "1 error expected"
    error = errors[0]
    assert "reason" in error, "reason expected"
    assert error["reason"] == "EXCEEDENT_VALUE", "EXCEEDENT_VALUE expected"
    assert "line" in error, "line expected"
    assert error["line"] == 1, "line 1 expected"
    assert "column" in error, "column expected"
    assert error["column"] == 15, "column 15 expected"
    assert "size" in error, "size expected"
    assert error["size"] == 9, "size 9 expected"


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
    assert error["column"] == 5, "column 1 expected"
    assert "size" in error, "size expected"
    assert error["size"] == 1, "size 1 expected"


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
    assert "line" in error, "line expected"
    assert error["line"] == 3, "line 3 expected"
    assert "column" in error, "column expected"
    assert error["column"] == 9, "column 9 expected"
    assert "size" in error, "size expected"
    assert error["size"] == 1, "size 1 expected"


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
    assert "line" in error, "line expected"
    assert error["line"] == 2, "line 2 expected"
    assert "column" in error, "column expected"
    assert error["column"] == 11, "column 11 expected"
    assert "size" in error, "size expected"
    assert error["size"] == 1, "size 1 expected"


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
    assert "line" in error, "line expected"
    assert error["line"] == 2, "line 2 expected"
    assert "column" in error, "column expected"
    assert error["column"] == 18, "column 18 expected"
    assert "size" in error, "size expected"
    assert error["size"] == 9, "size 1 expected"
