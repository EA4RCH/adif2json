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
            "tipes": {'myheader': 'S'},
        }
    }, res


def test_multiple_headers():
    imput = '<myheader:1>1\n<myheader2:2>12\n<EOH>\n'
    res = to_dict(imput)

    assert res == {
        "headers": {
            "fields": {'myheader': '1', 'myheader2': '12'},
            "tipes": {'myheader': 'S', 'myheader2': 'S'},
        }
    }, res


def test_first_header_bad_then_right():
    imput = '<bad:x>1\n<myheader:1>1\n<EOH>\n'
    res = to_dict(imput)

    assert res == {
        "headers": {
            "fields": {'myheader': '1'},
            "tipes": {'myheader': 'S'},
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
            "tipes": {'myheader': 'S'},
        },
        "errors": ['INVALID_SIZE'],
    }, res


def test_one_qso():
    imput = '<call:6>EA4HFF<EOR>'
    res = to_dict(imput)

    assert res == {
        "qsos": [
            { 'fields': {'call': 'EA4HFF'}, 'tipes': {'call': 'S'} }
        ]
    }, res
