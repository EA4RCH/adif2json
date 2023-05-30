from functools import reduce
from typing import Callable, Iterator, List, Optional, Tuple, TypeVar
from dataclasses import dataclass
from itertools import chain, dropwhile, takewhile


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


def __unpack(fun):
    def _fun(val):
        return fun(*val)

    return _fun


@dataclass
class FormatError:
    msg: str
    part: str


def parse_all(s: str) -> List[Field | FormatError | Eor | Eoh]:
    def _parse_record(s: str) -> Tuple[str, str]:
        try:
            lab, val = s.split(">", 1)
            return lab, val
        except ValueError:
            if len(s) == 0:
                return s, ""
        return "", ""

    def _parse_delimiters(s: str, v: str) -> Tuple[str | Eor | Eoh, str]:
        up = s.upper()
        if up == "EOH":
            return Eoh(), v
        elif up == "EOR":
            return Eor(), v
        return s, v

    def _parse_label(
        s: str | Eor | Eoh, v: str
    ) -> Tuple[Tuple[str, int, Optional[str]] | Eor | Eoh | FormatError, str]:
        if not isinstance(s, str):
            return s, v
        parts = s.split(":")
        name = parts[0]
        if len(name) == 0:
            return FormatError("Empty label", s), v
        try:
            size = int(parts[1])
        except ValueError:
            return FormatError("Size must be a non decimal number", s), v
        except IndexError:
            return FormatError("Expect size", s), v
        if len(parts) > 2:
            tipe = parts[2]
            if len(tipe) > 1 or not tipe[0].isalpha():
                return FormatError("Type must be one Character", s), v
        else:
            tipe = None
        return (name, size, tipe), v

    def _read_field(
        s: Tuple[str, int, Optional[str]] | Eor | Eoh, v: str
    ) -> List[Field | FormatError | Eor | Eoh]:
        if isinstance(s, Eor) or isinstance(s, Eoh):
            return [s]
        if isinstance(s, FormatError):
            return [s]
        out = []
        name, size, tipe = s
        valid = True

        if len(v) == 0:
            valid = False
            return [FormatError("Empty value", repr(s))]
        elif len(v) < size:
            size = len(v)
            out.append(FormatError("Truncated value", v))
        elif len(v) > size:
            remainder = v[size:]
            if len(remainder.strip()) > 0:
                out.append(FormatError("Exeedent value", remainder))

        value = v[:size]
        out.append(Field(name, value, tipe))
        return out

    def _reduce(acc, x):
        if isinstance(x, list):
            return acc + x
        return acc + [x]

    tags = s.split("<")
    records = map(_parse_record, tags[1:])
    delim = map(__unpack(_parse_delimiters), records)
    labeled = map(__unpack(_parse_label), delim)
    records = map(__unpack(_read_field), labeled)
    return list(reduce(_reduce, records, []))
