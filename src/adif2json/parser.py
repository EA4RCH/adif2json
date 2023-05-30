from typing import Iterator, List, Optional, Tuple
from dataclasses import dataclass
from itertools import dropwhile, takewhile


@dataclass
class Character:
    character: str
    line: int
    column: int


def stream_character(s: str | Iterator[str], l=0, c=0) -> Iterator[Character]:
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


@dataclass
class Field:
    name: str
    value: str
    tipe: Optional[str] = None


@dataclass
class Eoh:
    pass


@dataclass
class Eor:
    pass


@dataclass
class ParseError:
    msg: str
    segment: List[Character]


def parse_fields(c: Iterator[Character]) -> Iterator[Field | ParseError | Eor | Eoh]:
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

    ok = next(dropwhile(lambda x: not _open_tag(x), c), None)
    if ok is None:
        return
    while True:
        valid = True
        label = list(takewhile(lambda x: not _close_tag(x), c))
        if not label:
            return

        n_parts, parts = _split(label, ":")
        tipe = None
        size = None
        size_int = 0

        name = charlist_to_str(parts[0])
        if len(name) == 0:
            yield ParseError("Empty label", label)
            valid = False

        if n_parts == 1:
            if name.upper() == "EOH":
                yield Eoh()
            elif name.upper() == "EOR":
                yield Eor()
            else:
                yield ParseError("Expect size", parts[0])
            valid = False

        if n_parts > 1:
            size = parts[1]
            try:
                size_int = int(charlist_to_str(size))
            except ValueError:
                yield ParseError("Size must be a non decimal number", size)
                valid = False

        if n_parts > 2:
            tipe = parts[2]
            if len(tipe) > 1 or not tipe[0].character.isalpha():
                yield ParseError("Type must be one Character", tipe)
                valid = False
            tipe = charlist_to_str(tipe)

        if valid:
            remainder = list(takewhile(lambda x: not _open_tag(x), c))
            current_remainder = charlist_to_str(remainder).strip()
            value = current_remainder[:size_int]
            if size_int < len(current_remainder):
                yield ParseError("Excedeent value", remainder[size_int:])
            elif size_int > len(current_remainder):
                yield ParseError("Size is bigger than value", remainder)
                continue
            yield Field(name, value, tipe)
        else:
            ok = next(dropwhile(lambda x: not _open_tag(x), c), None)
            if ok is None:
                return
