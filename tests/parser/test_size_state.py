import adif2json.parser as p


def test_one_number():
    previous = list(p.stream_character("<call:"))
    name = previous[1:-1]
    s = p.Character("1", 1, 1)
    res = p.state_machine(p.Size(name, []), s)

    assert res == p.Size(name, [s])


def test_several_numbers():
    text = list(p.stream_character("<call:213"))
    name = text[1:5]
    size = text[6:-1]
    s = text[-1]
    res = p.state_machine(p.Size(name, size), s)

    assert res == p.Size(name, text[6:])


def test_invalid_size_state():
    text = list(p.stream_character("<call:213"))
    name = text[1:5]
    size = text[6:]
    s = p.Character("a", 1, 10)
    res = p.state_machine(p.Size(name, size), s)

    assert res == p.IvalidLabelSize(text[6:] + [s])


def invalid_size_first():
    text = list(p.stream_character("<call:x"))
    name = text[1:5]
    size = text[6:]
    s = p.Character("1", 1, 10)
    res = p.state_machine(p.Size(name, size), s)

    assert res == p.IvalidLabelSize(text[6:] + [s])


def test_simple_value():
    text = list(p.stream_character("<call:4"))
    name = text[1:5]
    size = text[6:]
    s = p.Character(">", 1, 10)
    res = p.state_machine(p.Size(name, size), s)

    assert res == p.Value(name, size, [], 4)


def test_just_tipe():
    text = list(p.stream_character("<call:4"))
    name = text[1:5]
    size = text[6:]
    s = p.Character(":", 1, 10)
    res = p.state_machine(p.Size(name, size), s)

    assert res == p.Tipe(name, size)
