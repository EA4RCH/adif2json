from typing import Any, Iterator, List, Optional, Tuple
from dataclasses import dataclass
from itertools import dropwhile, takewhile


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


def stream_character(s: str | Iterator[str]) -> Iterator[Character]:
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
class EmitState:
    pass


@dataclass
class Name:
    name: List[Character]


@dataclass
class IvalidLabel(EmitState):
    name: List[Character]


@dataclass
class Size:
    name: List[Character]
    size: List[Character]


@dataclass
class IvalidLabelSize(EmitState):
    size: List[Character]


@dataclass
class Tipe:
    name: List[Character]
    size: List[Character]
    tipe: Optional[Character] = None


@dataclass
class IvalidLabelTipe(EmitState):
    tipe: Character


@dataclass
class Value(EmitState):
    name: List[Character]
    size: List[Character]
    value: List[Character]
    current_size: int
    tipe: Optional[Character] = None


@dataclass
class TruncatedValue(EmitState):
    value: List[Character]


@dataclass
class Remainder:
    remainder: List[Character]


@dataclass
class ExceededValue(EmitState):
    remainder: List[Character]


@dataclass
class Eoh(EmitState):
    pass


@dataclass
class Eor(EmitState):
    pass


def _state(st: State, c: Iterator[Character]) -> Iterator[Name | EmitState]:
    """
    The fundamental state is discarding characters until we find a
    character <.
    """
    yield Name([])


def _name(st: Name, c: Iterator[Character]) -> Size | State | EmitState:
    """
    Reading the name, will accumulate chars until we find a >
    or a :.
    """

    def _end_part(x: Character) -> bool:
        if x.character == ">":
            return True
        elif x.character == ":":
            return True
        return False

    try:
        current = next(c)
    except StopIteration:
        return
    if current == "<":
        name = list(takewhile(_end_part, c))
        size = list(takewhile(_end_part, c))
        tipe = list(takewhile(_end_part, c))

        if is_char_seq_equals(map(lambda x: x.character.upper(), st.name), "EOH"):
            return State(), Eoh()
        elif is_char_seq_equals(map(lambda x: x.character.upper(), st.name), "EOR"):
            return State(), Eor()
        else:
            return State(), IvalidLabelSize(st.name)
    elif c.character == ":":
        if len(st.name) == 0:
            return State(), IvalidLabel([c])
        return Size(st.name, []), None
    else:
        st.name.append(c)
    return st, None


def _size(
    st: Size, c: Character
) -> Tuple[Size | Tipe | Value | State, Optional[EmitState]]:
    """
    Will keep acumulating chars until we find a : or a >.
    if we find a no numerical value (a-z) then will return an
    invalid size state
    """
    if c.character == ":":
        return Tipe(st.name, st.size), None
    elif c.character == ">":
        n = int(charlist_to_str(st.size))
        return Value(st.name, st.size, [], n), None
    elif c.character.isdigit():
        st.size.append(c)
    else:
        return State(), IvalidLabelSize(st.size + [c])
    return st, None


def _tipe(st: Tipe, c: Character) -> Tuple[Tipe | Value | State, Optional[EmitState]]:
    """
    Tipe is a one character string. Represent the type of the value.
    if we find a no numerical value (a-z) then will return an
    invalid tipe state.
    if we find a second character then will return an invalid tipe
    """
    if c.character == ">":
        if st.tipe is None:
            return State(), IvalidLabelTipe(c)
        n = int(charlist_to_str(st.size))
        return Value(st.name, st.size, [], n, st.tipe), None
    elif c.character.isdigit():
        return State(), IvalidLabelTipe(c)
    elif st.tipe is None:
        st.tipe = c
        return st, None
    return State(), IvalidLabelTipe(c)


def _value(
    st: Value, c: Character
) -> Tuple[Value | Name | Remainder, Optional[EmitState]]:
    """
    Will read the value until size is reached.
    if we find a < and size is greater than 0 then will return a
    TruncatedValue state.
    when size is reached will return a Remainder state.
    """
    if c.character == "<":
        if st.current_size > 0:
            return Name([]), TruncatedValue(st.value)
        else:
            return Name([]), st
    elif st.current_size == 0:
        return Remainder([c]), st
    else:
        st.value.append(c)
        st.current_size -= 1
    return st, None


def _remainder(
    st: Remainder, c: Character
) -> Tuple[Remainder | Name | ExceededValue, Optional[EmitState]]:
    """
    Will read the value until size is reached.
    if we find a < and size is greater than 0 then will return a
    TruncatedValue state.
    Will only add characters to the value. No spaces, tabs or newlines.
    """
    if c.character == "<":
        rem = charlist_to_str(st.remainder).strip()
        if len(rem) > 0:
            return Name([]), ExceededValue(st.remainder)
        else:
            return Name([]), None
    elif not c.character.isspace():
        if not st.remainder:
            st.remainder = []
        st.remainder.append(c)
    return st, None


DISPATCHERS = {
    Name: _name,
    Size: _size,
    Value: _value,
    Remainder: _remainder,
    State: _state,
    Tipe: _tipe,
}


def state_machine(char: Iterator[Character]) -> Tuple[Any, Any]:
    """
    TODO: state reading must be stiky. The machine must read
    until find their end state.
    Is better to yield instear or return, so we can emit several
    things as needed ???
    """
    raise NotImplementedError


def parse_fields(c: Iterator[Character]) -> Iterator[str | EmitState]:
    def _open_tag(x: Character) -> bool:
        return x.character == "<"

    def _close_tag(x: Character) -> bool:
        return x.character == ">"

    def _split(xs: List[Character], s: str) -> Tuple[int, List[List[Character]]]:
        res = [[]]
        i = 0
        for x in xs:
            if x.character == s:
                res.append([])
                i += 1
            else:
                res[i].append(x)
        return len(res), res

    while True:
        ok = next(dropwhile(lambda x: not _open_tag(x), c), None)
        if ok is None:
            return
        label = list(takewhile(lambda x: not _close_tag(x), c))
        n_parts, parts = _split(label, ":")
        tipe = None
        size = None
        size_int = 0
        if n_parts == 1:
            name = charlist_to_str(parts[0])
            if name.upper() == "EOH":
                yield Eoh()
            elif name.upper() == "EOR":
                yield Eor()
            else:
                yield IvalidLabelSize(parts[0])
            continue
        if n_parts > 1:
            name = charlist_to_str(parts[0])
            size = parts[1]
            try:
                size_int = int(charlist_to_str(size))
            except ValueError:
                yield IvalidLabelSize(size)
                continue
        if n_parts > 2:
            tipe = parts[2]

        remainder = list(takewhile(lambda x: not _open_tag(x), c))
        current_remainder = charlist_to_str(remainder).strip()
        if size_int < len(current_remainder):
            yield ExceededValue(remainder)
            continue
        elif size_int > len(current_remainder):
            yield TruncatedValue(remainder)
            continue
        value = current_remainder[:size_int]

        yield name
        yield tipe
        yield value
