import adif2json.parser as p


def test_zero_size_value():
    text = list(p.stream_character("<call:0>"))
    name = text[1:5]
    size = text[6:-1]
    s = p.Character(" ", 1, 10)
    res, em = p.state_machine(p.Value(name, size, [], 0), s)

    assert res == p.Remainder([s])
    assert em == p.Value(name, size, [], 0)


def test_read_first_value_char():
    text = list(p.stream_character("<call:4>"))
    name = text[1:5]
    size = text[6:-1]
    s = p.Character("A", 1, 10)
    res, em = p.state_machine(p.Value(name, size, [], 4), s)

    assert res == p.Value(name, size, [s], 3)
    assert em is None


def test_last_value_char():
    text = list(p.stream_character("<call:4>EC5"))
    name = text[1:5]
    size = text[6:7]
    value = text[7:]
    s = p.Character("A", 1, 12)
    # ugly side effect, value is modified
    res, em = p.state_machine(p.Value(name, size, value, 1), s)

    assert res == p.Value(name, size, value, 0)
    assert em is None


def test_enter_remainder():
    text = list(p.stream_character("<call:4>EC5A"))
    name = text[1:5]
    size = text[6:7]
    value = text[7:]
    s = p.Character(" ", 1, 13)

    res, em = p.state_machine(p.Value(name, size, value, 0), s)

    assert res == p.Remainder([s])
    assert em == p.Value(name, size, value, 0)


def test_truncated_value():
    text = list(p.stream_character("<call:4>EC5"))
    name = text[1:5]
    size = text[6:7]
    value = text[7:]
    s = p.Character("<", 1, 12)
    # ugly side effect, value is modified
    res, em = p.state_machine(p.Value(name, size, value, 1), s)

    assert res == p.Name([])
    assert em == p.TruncatedValue(value)