import logging
import re
from typing import Iterable, Optional, Tuple
from dataclasses import dataclass


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


def __unpack(fun):
    def _fun(val):
        return fun(*val)

    return _fun


@dataclass
class FormatError:
    msg: str
    part: str


def _iter_finder_stream(s: Iterable[str]) -> Iterable[Tuple[str, str]]:
    logging.debug(f"Iter fields stream")
    rest = ""
    for l in s:
        tofind = rest + l
        labels = tofind.split("<")
        for p in labels:
            parts = p.split(">")
            if len(parts) == 1:
                rest = parts[0]
            else:
                label, value = parts
                yield label, value

    logging.debug(f"Iter fields done")


def _iter_finder(s: str) -> Iterable[Tuple[str, str]]:
    logging.debug(f"Iter fields")
    for l in re.finditer(r"([^<]*)>([^<]*)", s):
        yield l.group(1), l.group(2)
    logging.debug(f"Iter fields done")


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
    logging.debug(f"Parsing label {s} parts {len(parts)}")
    name = parts[0]
    if len(name) == 0:
        logging.error(f"Empty label {s}")
        return FormatError("Empty label", s), v
    try:
        size = int(parts[1])
    except ValueError:
        logging.error(f"Size must be a non decimal number {s}")
        return FormatError("Size must be a non decimal number", s), v
    except IndexError:
        logging.error(f"Expect size {s}")
        return FormatError("Expect size", s), v
    if len(parts) > 2:
        tipe = parts[2]
        if len(tipe) > 1 or not tipe[0].isalpha():
            logging.error(f"Type must be one Character {s}")
            return FormatError("Type must be one Character", s), v
        logging.debug(f"Type {tipe}")
    else:
        tipe = None
    return (name, size, tipe), v


def _read_field(
    s: Tuple[str, int, Optional[str]] | FormatError | Eor | Eoh, v: str
) -> Iterable[Field | FormatError | Eor | Eoh]:
    logging.debug(f"Reading field {s} value {v}")
    if isinstance(s, Eor) or isinstance(s, Eoh):
        yield s
        return
    if isinstance(s, FormatError):
        yield s
        return
    name, size, tipe = s

    if size != 0 and len(v) == 0:
        logging.error(f"Empty value {repr(s)}")
        yield FormatError("Empty value", repr(s))
        return
    elif len(v) < size:
        size = len(v)
        logging.error(f"Truncated value {v}")
        logging.debug(f"Resize field to available info {v}")
        yield FormatError("Truncated value", v)
    elif len(v) > size:
        remainder = v[size:]
        if len(remainder.strip()) > 0:
            logging.error(f"Exeedent value {remainder}")
            yield FormatError("Exeedent value", remainder)

    value = v[:size]
    logging.debug(f"Field {name} value {value}")
    yield Field(name, value, tipe)


def parse_all(s: Iterable[str]) -> Iterable[Field | FormatError | Eor | Eoh]:
    if s == "":
        return
    tags = _iter_finder_stream(s)
    delim = map(__unpack(_parse_delimiters), tags)
    labeled = map(__unpack(_parse_label), delim)
    records = map(__unpack(_read_field), labeled)
    for x in records:
        yield from x
