import adif2json.parser as p


def test_spaces():
    s = p.Character(" ", 1, 1)
    res = p.state_machine(p.Remainder([], [], []), s)

    assert res == p.Remainder([], [], [], None, None)


def test_any_character():
    s = p.Character("a", 1, 1)
    res = p.state_machine(p.Remainder([], [], []), s)

    assert res == p.Remainder([], [], [], None, [s])


def test_back_to_name():
    s = p.Character("<", 1, 1)
    res = p.state_machine(p.Remainder([], [], []), s)

    assert res == p.Name([])


def test_exceeded_value():
    text = list(p.stream_character("there is more text "))
    s = p.Character("<", 1, 20)
    inp = p.Remainder([], [], [], None, text)
    res = p.state_machine(inp, s)

    assert res == p.ExceededValue(text)
