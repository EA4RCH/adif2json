import adif2json.parser as p


def test_spaces():
    s = p.Character(" ", 1, 1)
    res, em = p.state_machine(p.Remainder([]), s)

    assert res == p.Remainder([])
    assert em is None


def test_any_character():
    s = p.Character("a", 1, 1)
    res, em = p.state_machine(p.Remainder([]), s)

    assert res == p.Remainder([s])
    assert em is None


def test_back_to_name():
    s = p.Character("<", 1, 1)
    res, em = p.state_machine(p.Remainder([]), s)

    assert res == p.Name([])
    assert em is None


def test_exceeded_value():
    text = list(p.stream_character("there is more text "))
    s = p.Character("<", 1, 20)
    inp = p.Remainder(text)
    res, em = p.state_machine(inp, s)

    assert res == p.Name([])
    assert em == p.ExceededValue(text)
