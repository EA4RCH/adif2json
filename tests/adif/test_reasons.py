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
    # TODO: check error


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
    # TODO: check error
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
    # TODO: check error
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
    # TODO: check error
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

    res_l = list(to_dict(imput))

    assert len(res_l) == 3
    res = res_l[0]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EA4HFF", "band": "40m"}
    assert res["errors"] is None
    res = res_l[1]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EA4AW", "band": "40m"}
    assert res["errors"] is None
    res = res_l[2]
    assert res["type"] == "qso"
    assert res["fields"] == {"band": "40m"}
    assert res["errors"] is not None
    assert len(res["errors"]) == 1
    # TODO: check error


def test_report_invalid_size_multifield():
    imput = """
    <call:6>EA4HFF<band:3>40m<EOR>
    <call:x>EA4AW<band:3>40m<EOR>
    <call:4>EC5A<band:3>40m<EOR>
    """

    res_l = list(to_dict(imput))

    assert len(res_l) == 3
    res = res_l[0]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EA4HFF", "band": "40m"}
    assert res["errors"] is None
    res = res_l[1]
    assert res["type"] == "qso"
    assert res["fields"] == {"band": "40m"}
    assert res["errors"] is not None
    assert len(res["errors"]) == 1
    # TODO: check error
    res = res_l[2]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EC5A", "band": "40m"}
    assert res["errors"] is None


def test_report_invalid_type_multifield():
    imput = """
    <call:6:8>EA4HFF<band:3>40m<EOR>
    <call:5>EA4AW<band:3>40m<EOR>
    <call:4>EC5A<band:3>40m<EOR>
    """

    res_l = list(to_dict(imput))

    assert len(res_l) == 3
    res = res_l[0]
    assert res["type"] == "qso"
    assert res["fields"] == {"band": "40m"}
    assert len(res["errors"]) == 1
    # TODO: check error
    res = res_l[1]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EA4AW", "band": "40m"}
    assert res["errors"] is None
    res = res_l[2]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EC5A", "band": "40m"}
    assert res["errors"] is None


def test_report_exceedent_value_multifield():
    imput = """
    <call:6>EA4HFF tha best<band:3>40m<EOR>
    <call:5>EA4AW<band:3>40m<EOR>
    <call:4>EC5A<band:3>40m<EOR>
    """

    res_l = list(to_dict(imput))

    assert len(res_l) == 3
    res = res_l[0]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EA4HFF", "band": "40m"}
    assert len(res["errors"]) == 1
    # TODO: check error
    res = res_l[1]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EA4AW", "band": "40m"}
    assert res["errors"] is None
    res = res_l[2]
    assert res["type"] == "qso"
    assert res["fields"] == {"call": "EC5A", "band": "40m"}
    assert res["errors"] is None
