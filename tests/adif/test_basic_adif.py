from adif2json.adif import to_dict


def test_empty():
    imput = ''
    res = to_dict(imput)

    assert res == {}


def test_simplest_empty_headers():
    imput = '<EOH>\n'
    res = to_dict(imput)

    assert res == {"headers": []}


def test_simplest_empty_headers_with_space():
    imput = '<EOH>         \n'
    res = to_dict(imput)

    assert res == {"headers": []}


def test_one_header():
    imput = '<myheader:1>1\n<EOH>\n'
    res = to_dict(imput)

    assert res == {"headers": [{'label': 'myheader', 'tipe': None, 'value': '1'}]}
