import adif2json.parser as p


def test_one_char_tipe():
    text = list(p.stream_character("<call:4:"))
    name = text[1:5]
    size = text[6:-1]
    s = p.Character("A", 1, 10)
    res = p.state_machine(p.Tipe(name, size), s)

    assert res == p.Tipe(name, size, s)


def test_several_chars_tipe():
    text = list(p.stream_character("<call:4:S"))
    name = text[1:5]
    size = text[6:-1]
    s = p.Character("B", 1, 11)
    res = p.state_machine(p.Tipe(name, size, text[-1]), s)

    assert res == p.IvalidLabelTipe(s)


def test_digit_tipe():
    text = list(p.stream_character("<call:4:"))
    name = text[1:5]
    size = text[6:-1]
    s = p.Character("1", 1, 10)
    res = p.state_machine(p.Tipe(name, size), s)

    assert res == p.IvalidLabelTipe(s)


def test_tipe_value():
    text = list(p.stream_character("<call:4:S"))
    name = text[1:5]
    size = text[6:-2]
    s = p.Character(">", 1, 11)
    res = p.state_machine(p.Tipe(name, size, text[-1]), s)

    assert res == p.Value(name, size, [], 4, text[-1])
