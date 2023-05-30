import logging
from functools import reduce
from typing import List, Optional, Tuple
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


def __parse_record(s: str) -> Tuple[str, str]:
    try:
        lab, val = s.split(">", 1)
        return lab, val
    except ValueError:
        if len(s) == 0:
            return s, ""
    return "", ""


def __parse_delimiters(s: str, v: str) -> Tuple[str | Eor | Eoh, str]:
    up = s.upper()
    if up == "EOH":
        return Eoh(), v
    elif up == "EOR":
        return Eor(), v
    return s, v


def __parse_label(
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


def __read_field(
    s: Tuple[str, int, Optional[str]] | Eor | Eoh, v: str
) -> List[Field | FormatError | Eor | Eoh]:
    logging.debug(f"Reading field {s} value {v}")
    if isinstance(s, Eor) or isinstance(s, Eoh):
        return [s]
    if isinstance(s, FormatError):
        return [s]
    out = []
    name, size, tipe = s

    if len(v) == 0:
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


def __reduce(acc, x):
    return acc + x


def parse_all(s: str) -> List[Field | FormatError | Eor | Eoh]:

    logging.info("Start parsing")
    tags = s.split("<")
    logging.info(f"potencial fields {len(tags)}")
    records = map(__parse_record, tags[1:])
    delim = map(__unpack(__parse_delimiters), records)
    labeled = map(__unpack(__parse_label), delim)
    records = list(map(__unpack(__read_field), labeled))
    logging.info(f"fields {len(records)}")
    out = [item for sublist in records for item in sublist]
    logging.info("Done parsing")
    return out
