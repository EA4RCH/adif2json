from adif2json.adif import to_dict


def test_empty():
    imput = ''
    res = to_dict(imput)

    assert res == {}


def test_simplest_empty_headers():
    imput = '<EOH>\n'
    res = to_dict(imput)

    assert res == {"headers": None}


def test_simplest_empty_headers_with_space():
    imput = '<EOH>         \n'
    res = to_dict(imput)

    assert res == {"headers": None}


def test_one_header():
    imput = '<myheader:1>1\n<EOH>\n'
    res = to_dict(imput)

    assert res == {
        "headers": {
            "fields": {'myheader': '1'},
        }
    }, res


def test_multiple_headers():
    imput = '<myheader:1>1\n<myheader2:2>12\n<EOH>\n'
    res = to_dict(imput)

    assert res == {
        "headers": {
            "fields": {'myheader': '1', 'myheader2': '12'},
        }
    }, res


def test_first_header_bad_then_right():
    imput = '<bad:x>1\n<myheader:1>1\n<EOH>\n'
    res = to_dict(imput)

    assert res == {
        "headers": {
            "fields": {'myheader': '1'},
        },
        "errors": ['INVALID_SIZE'],
    }, res


def test_all_bad_headers():
    imput = '<bad:x>1\n<bad2:x>12\n<EOH>\n'
    res = to_dict(imput)

    assert res == {
        "headers": None,
        "errors": ['INVALID_SIZE', 'INVALID_SIZE'],
    }, res


def test_last_bad_header():
    imput = '<myheader:1>1\n<bad:x>12\n<EOH>\n'
    res = to_dict(imput)

    assert res == {
        "headers": {
            "fields": {'myheader': '1'},
        },
        "errors": ['INVALID_SIZE'],
    }, res


def test_one_qso():
    imput = '<call:6>EA4HFF<EOR>'
    res = to_dict(imput)

    assert res == {
        "qsos": [
            { 'fields': {'call': 'EA4HFF'} }
        ]
    }, res


def test_several_qsos():
    imput = '<call:6>EA4HFF<EOR><call:5>EA4AW<EOR><call:4>EC5A<EOR>'
    res = to_dict(imput)

    assert res == {
        "qsos": [
            { 'fields': {'call': 'EA4HFF'} },
            { 'fields': {'call': 'EA4AW'} },
            { 'fields': {'call': 'EC5A'} },
        ]
    }, res


def test_headers_and_qsos():
    imput = '<program:9>aidf2json<EOH><call:6>EA4HFF<EOR><call:5>EA4AW<EOR><call:4>EC5A<EOR>'
    res = to_dict(imput)

    assert res == {
        "headers": {
            "fields": {'program': 'aidf2json'},
        },
        "qsos": [
            { 'fields': {'call': 'EA4HFF'} },
            { 'fields': {'call': 'EA4AW'} },
            { 'fields': {'call': 'EC5A'} },
        ]
    }
