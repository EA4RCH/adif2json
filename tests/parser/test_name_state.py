import adif2json.parser as p


def test_one_char():
    s = p.Character("a", 1, 1)
    res, em = p.state_machine(p.Name([]), s)

    assert res == p.Name([s])
    assert em is None


def test_append_chars():
    s = p.Character("a", 1, 1)
    res, em = p.state_machine(p.Name([s]), s)

    assert res == p.Name([s, s])
    assert em is None


def test_close_label_character_eoh():
    acc = list(p.stream_character("eoh"))
    s = p.Character(">", 1, 4)
    res, em = p.state_machine(p.Name(acc), s)

    assert res == p.State()
    assert em == p.Eoh()


def test_close_label_character_eor():
    acc = list(p.stream_character("eor"))
    s = p.Character(">", 1, 4)
    res, em = p.state_machine(p.Name(acc), s)

    assert res == p.State()
    assert em == p.Eor()


def test_invalid_no_size_label():
    acc = list(p.stream_character("<call"))
    s = p.Character(">", 1, 5)
    res, em = p.state_machine(p.Name(acc[1:]), s)

    assert res == p.State()
    assert em == p.IvalidLabelSize(acc[1:])


def test_to_size_label():
    acc = list(p.stream_character("<call"))
    s = p.Character(":", 1, 6)
    res, em = p.state_machine(p.Name(acc[1:]), s)

    assert res == p.Size(acc[1:], [])
    assert em is None
