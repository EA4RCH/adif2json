import adif2json.parser as par


def test_emtpy():
    res = list(par._iter_finder_stream([""]))

    assert res == []


def test_simple_w_headers():
    imp = [
        "<header1:5>12345 <EOH>",
        "<field1:5>12345 <EOR>",
    ]
    res = list(par._iter_finder_stream(imp))

    assert res == [
        ("header1:5", "12345 "),
        ("EOH", ""),
        ("field1:5", "12345 "),
        ("EOR", ""),
    ]


def test_simple_wo_headers():
    imp = [
        "<field1:5>12345 <EOR>",
    ]
    res = list(par._iter_finder_stream(imp))

    assert res == [
        ("field1:5", "12345 "),
        ("EOR", ""),
    ]


def test_truncated_text():
    imp = ["<field1:5>1234 <EO", "R>"]
    res = list(par._iter_finder_stream(imp))

    assert res == [
        ("field1:5", "1234 "),
        ("EOR", ""),
    ]
