from typing import Any, Iterator, List, Optional, Tuple
from dataclasses import dataclass
from functools import singledispatch


@dataclass
class Position:
    remaining: str
    line: int = 1
    column: int = 1


@dataclass
class EndOfFile:
    line: int
    column: int


def discard_until(p: Position, c: str) -> Position | EndOfFile:
    """
    Discard characters from the start of the string until one of the
    characters in chars is found. Return the remaining string.
    It will keep the first character that matches; use discard_forward
    to discard that character as well.
    """
    _, res = read_until(p, c)
    return res


def discard_forward(p: Position, c: str) -> Position | EndOfFile:
    """
    Discard characters from the start of the string until one of the
    characters in chars is found. Return the remaining string.
    It will discard the first character that matches; use discard_until
    to keep that character.
    """
    _, res = read_forward(p, c)
    return res


def read_until(p: Position, c: str) -> Tuple[str, Position | EndOfFile]:
    """
    Read characters from the start of the string until one of the
    characters in chars is found. Return the characters read and the
    remaining string.
    """
    idx = p.remaining.find(c)
    if idx == -1:
        line, col = _update_position(p.remaining, p.line, p.column)
        return p.remaining, EndOfFile(line, col)
    res, rem = read_n(p, idx)
    return res, rem


def read_forward(p: Position, c: str) -> Tuple[str, Position | EndOfFile]:
    """
    Read characters from the start of the string until one of the
    characters in chars is found. Return the characters read and the
    remaining string.
    """
    res, rem = read_until(p, c)
    if isinstance(rem, EndOfFile):
        return res, rem
    line, col = _update_position(rem.remaining[0], rem.line, rem.column)
    p = Position(rem.remaining[1:], line, col)
    return res + rem.remaining[0], p


def _update_position(s: str, line: int, column: int) -> Tuple[int, int]:
    if s == "":
        return line, column
    else:
        if line == 0:
            line = 1
        if column == 0:
            column = 1
    while len(s) > 0:
        if s[0] == "\n":
            line += 1
            column = 0
        else:
            column += 1
        s = s[1:]
    return line, column


def read_n(p: Position, n: int) -> Tuple[str, Position | EndOfFile]:
    """
    Must read n characters from the start of the string. Return the
    characters read and the remaining string.
    """
    if len(p.remaining) < n:
        line, col = _update_position(p.remaining, p.line, p.column)
        return p.remaining, EndOfFile(line, col)
    line, col = _update_position(p.remaining[:n], p.line, p.column)
    return p.remaining[:n], Position(p.remaining[n:], line, col)


def discard_n(p: Position, n: int) -> Position | EndOfFile:
    """
    Must discard n characters from the start of the string. Return the
    remaining string.
    """
    _, res = read_n(p, n)
    return res


@dataclass
class Character:
    character: str
    line: int
    column: int


def stream_character(s: str) -> Iterator[Character]:
    l = 0
    c = 0
    for s in s:
        if l == 0:
            l = 1
        if s == "\n":
            l += 1
            c = 0
        else:
            c += 1
        yield Character(s, l, c)


def is_char_seq_equals(s1: Iterator[str], s2: str) -> bool:
    """
    Compare two strings, one is an iterator of characters, the other
    is a string.
    """
    for c1, c2 in zip(s1, s2):
        if c1 != c2:
            return False
    return True


def charlist_to_str(l: List[Character]) -> str:
    return "".join([c.character for c in l])


# State machine approach
@dataclass
class State:
    pass


@dataclass
class Name:
    name: List[Character]


@dataclass
class IvalidLabel:
    name: List[Character]


@dataclass
class Size:
    name: List[Character]
    size: List[Character]


@dataclass
class IvalidLabelSize:
    size: List[Character]


@dataclass
class Tipe:
    name: List[Character]
    size: List[Character]
    tipe: Optional[Character] = None


@dataclass
class IvalidLabelTipe:
    tipe: Character


@dataclass
class Value:
    name: List[Character]
    size: List[Character]
    value: List[Character]
    current_size: int
    tipe: Optional[Character] = None


@dataclass
class TruncatedValue:
    value: List[Character]


@dataclass
class Remainder:
    name: List[Character]
    size: List[Character]
    value: List[Character]
    tipe: Optional[Character] = None
    remainder: Optional[List[Character]] = None


@dataclass
class ExceededValue:
    remainder: List[Character]


@dataclass
class Eoh:
    pass


@dataclass
class Eor:
    pass


@singledispatch
def state_machine(_: Any, __: Any) -> Any:
    raise NotImplementedError


@state_machine.register
def _(st: State, c: Character) -> State | Name:
    """
    The fundamental state is discarding characters until we find a
    character <.
    """
    if c.character == "<":
        return Name([])
    return st


@state_machine.register
def _(st: Name, c: Character) -> Eoh | Eor | IvalidLabelSize | Size | Name:
    """
    Reading the name, will accumulate chars until we find a >
    or a :.
    """
    if c.character == ">":
        if is_char_seq_equals(map(lambda x: x.character.upper(), st.name), "EOH"):
            return Eoh()
        elif is_char_seq_equals(map(lambda x: x.character.upper(), st.name), "EOR"):
            return Eor()
        else:
            return IvalidLabelSize(st.name)
    elif c.character == ":":
        return Size(st.name, [])
    else:
        st.name.append(c)
    return st


@state_machine.register
def _(st: Size, c: Character) -> Size | Tipe | Value | IvalidLabelSize:
    """
    Will keep acumulating chars until we find a : or a >.
    if we find a no numerical value (a-z) then will return an
    invalid size state
    """
    if c.character == ":":
        return Tipe(st.name, st.size)
    elif c.character == ">":
        n = int(charlist_to_str(st.size))
        return Value(st.name, st.size, [], n)
    elif c.character.isdigit():
        st.size.append(c)
    else:
        return IvalidLabelSize(st.size + [c])
    return st


@state_machine.register
def _(st: Tipe, c: Character) -> Tipe | Value | IvalidLabelTipe:
    """
    Tipe is a one character string. Represent the type of the value.
    if we find a no numerical value (a-z) then will return an
    invalid tipe state.
    if we find a second character then will return an invalid tipe
    """
    if c.character == ">":
        if st.tipe is None:
            return IvalidLabelTipe(c)
        n = int(charlist_to_str(st.size))
        return Value(st.name, st.size, [], n, st.tipe)
    elif c.character.isdigit():
        return IvalidLabelTipe(c)
    elif st.tipe is None:
        st.tipe = c
        return st
    return IvalidLabelTipe(c)


@state_machine.register
def _(st: Value, c: Character) -> Value | TruncatedValue | Remainder:
    """
    Will read the value until size is reached.
    if we find a < and size is greater than 0 then will return a
    TruncatedValue state.
    when size is reached will return a Remainder state.
    """
    if c.character == "<":
        if st.current_size > 0:
            return TruncatedValue(st.value)
        else:
            return Remainder(st.name, st.size, st.value, st.tipe)
    elif st.current_size == 0:
        return Remainder(st.name, st.size, st.value, st.tipe)
    else:
        st.value.append(c)
        st.current_size -= 1
    return st


@state_machine.register
def _(st: Remainder, c: Character) -> Remainder | Name | ExceededValue:
    """
    Will read the value until size is reached.
    if we find a < and size is greater than 0 then will return a
    TruncatedValue state.
    Will only add characters to the value. No spaces, tabs or newlines.
    """
    if c.character == "<":
        if st.remainder and len(st.remainder) > 0:
            return ExceededValue(st.remainder)
        else:
            return Name([])
    elif not c.character.isspace():
        if not st.remainder:
            st.remainder = []
        st.remainder.append(c)
    return st
