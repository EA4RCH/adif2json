from adif2json.parser import Character, state_machine, State, Name

import pytest


def test_empty_string():
    s = Character("", 0, 0)
    res = state_machine(State(), s)

    assert res == State()


def test_one_character():
    s = Character("a", 1, 1)
    res = state_machine(State(), s)

    assert res == State()


def test_open_label_character():
    s = Character("<", 1, 1)
    res = state_machine(State(), s)

    assert res == Name([])


def test_unrecognized_state():
    with pytest.raises(NotImplementedError):
        state_machine({}, "a")
