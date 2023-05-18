from adif2json.adif import to_dict


def test_report_invalid_label():
    imput = '<call:6>EA4HFF<EOR><call:5>EA4AW<EOR><:4>EC5A<EOR>'

    res = to_dict(imput)

    assert res == {
        "qsos": [
            {'fields': {'call': 'EA4HFF'}},
            {'fields': {'call': 'EA4AW'}},
        ],
        "errors": ['INVALID_LABEL'],
    }, res


def test_report_invalid_size():
    imput = '<call:6>EA4HFF<EOR><call:x>EA4AW<EOR><call:4>EC5A<EOR>'

    res = to_dict(imput)

    assert res == {
        "qsos": [
            {'fields': {'call': 'EA4HFF'}},
            {'fields': {'call': 'EC5A'}},
        ],
        "errors": ['INVALID_SIZE'],
    }, res


def test_report_invalid_type():
    imput = '<call:6:8>EA4HFF<EOR><call:5>EA4AW<EOR><call:4>EC5A<EOR>'

    res = to_dict(imput)

    assert res == {
        "qsos": [
            {'fields': {'call': 'EA4AW'}},
            {'fields': {'call': 'EC5A'}},
        ],
        "errors": ['INVALID_TIPE'],
    }, res


def test_report_exceedent_value():
    imput = '<call:6>EA4HFF tha best<EOR><call:5>EA4AW<EOR><call:4>EC5A<EOR>'

    res = to_dict(imput)

    assert res == {
        "qsos": [
            {'fields': {'call': 'EA4AW'}},
            {'fields': {'call': 'EC5A'}},
        ],
        "errors": ['EXCEEDENT_VALUE'],
    }, res


def test_report_invalid_label_multifield():
    imput = """
    <call:6>EA4HFF<band:3>40m<EOR>
    <call:5>EA4AW<band:3>40m<EOR>
    <:4>EC5A<band:3>40m<EOR>
    """

    res = to_dict(imput)

    assert res == {
        "qsos": [
            {'fields': {'call': 'EA4HFF', 'band': '40m'}},
            {'fields': {'call': 'EA4AW', 'band': '40m'}},
            {'fields': {'band': '40m'}},
        ],
        "errors": ['INVALID_LABEL'],
    }, res


def test_report_invalid_size_multifield():
    imput = """
    <call:6>EA4HFF<band:3>40m<EOR>
    <call:x>EA4AW<band:3>40m<EOR>
    <call:4>EC5A<band:3>40m<EOR>
    """

    res = to_dict(imput)

    assert res == {
        "qsos": [
            {'fields': {'call': 'EA4HFF', 'band': '40m'}},
            {'fields': {'band': '40m'}},
            {'fields': {'call': 'EC5A', 'band': '40m'}},
        ],
        "errors": ['INVALID_SIZE'],
    }, res


def test_report_invalid_type_multifield():
    imput = """
    <call:6:8>EA4HFF<band:3>40m<EOR>
    <call:5>EA4AW<band:3>40m<EOR>
    <call:4>EC5A<band:3>40m<EOR>
    """

    res = to_dict(imput)

    assert res == {
        "qsos": [
            {'fields': {'band': '40m'}},
            {'fields': {'call': 'EA4AW', 'band': '40m'}},
            {'fields': {'call': 'EC5A', 'band': '40m'}},
        ],
        "errors": ['INVALID_TIPE'],
    }, res


def test_report_exceedent_value_multifield():
    imput = """
    <call:6>EA4HFF tha best<band:3>40m<EOR>
    <call:5>EA4AW<band:3>40m<EOR>
    <call:4>EC5A<band:3>40m<EOR>
    """

    res = to_dict(imput)

    assert res == {
        "qsos": [
            {'fields': {'band': '40m'}},
            {'fields': {'call': 'EA4AW', 'band': '40m'}},
            {'fields': {'call': 'EC5A', 'band': '40m'}},
        ],
        "errors": ['EXCEEDENT_VALUE'],
    }, res
