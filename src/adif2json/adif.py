import adif2json.parser as par


import json
from enum import Enum
from typing import Optional, Tuple, Dict, List
from dataclasses import dataclass, asdict


class Reason(Enum):
    EOF = 1
    EOH = 2
    EOR = 3
    INVALID_LABEL = 4
    INVALID_SIZE = 5
    INVALID_TIPE = 6
    INVALID_VALUE = 7


@dataclass
class Label:
    label: str
    size: Optional[int] = None
    tipe: Optional[str] = None


@dataclass
class Field:
    label: str
    value: str
    tipe: Optional[str] = None


@dataclass
class Record:
    fields: Dict[str, str]
    types: Dict[str, Optional[str]]


@dataclass
class Adif:
    headers: Optional[Record] = None
    qsos: Optional[List[Record]] = None
    errors: Optional[List[Reason]] = None


def to_json(adif: str) -> str:
    if adif == "": return "{\"qsos\": []}"
    d = to_dict(adif)
    return json.dumps(d)


def to_dict(adif: str) -> Dict:
    adif_f = _read_fields(adif)
    out = {}
    if adif_f.headers:
        if len(adif_f.headers.fields) > 0:
            out["headers"] = asdict(adif_f.headers)
        else:
            out["headers"] = None
    if adif_f.qsos:
        out["qsos"] = [asdict(qso) for qso in adif_f.qsos]
    if adif_f.errors:
        out["errors"] = [error.name for error in adif_f.errors]
    return out


def _read_fields(adif: str) -> Adif:
    if adif == "": return Adif()
    current : Record = Record({}, {})
    headers : Optional[Record] = None
    qsos = []
    errors = []
    rest = adif

    while True:
        field, rest = _read_field(rest)
        if isinstance(field, Reason):
            if field == Reason.EOF:
                return Adif(headers, qsos, errors)
            elif field == Reason.EOH:
                headers = current
                current = Record({}, {})
            elif field == Reason.EOR:
                qsos.append(current)
                current = Record({}, {})
            else:
                errors.append(field)
            continue

        current.fields[field.label] = field.value
        current.types[field.label] = field.tipe
    raise Exception("Unexpected")


def _read_field(adif: str) -> Tuple[Field | Reason, str]:
    label, rest =  _read_label(adif)
    if isinstance(label, Reason):
        return label, rest
    if not label.size:
        if label.label.upper() == "EOH":
            return Reason.EOH, rest
        if label.label.upper() == "EOR":
            return Reason.EOR, rest

    if label.size and label.size > 0:
        value, rest = _read_value(rest, label.size)
        if isinstance(value, Reason):
            return value, rest
        return Field(label.label, value, label.tipe), rest
    raise Exception("Unexpected")


def _read_label(adif: str) -> Tuple[Label | Reason, str]:
    rest = par.discard_forward(adif, '<')
    if not rest:
        return Reason.EOF, ""

    maybe_content = par.read_until(rest, '>')
    if not maybe_content:
        return Reason.EOF, ""

    content, rest = maybe_content
    if not content:
        return Reason.INVALID_LABEL, rest

    parts = content.split(':')
    rest = rest[1:]
    label = ""
    size = None
    tipe = None

    if len(parts) >= 1:
        label = parts[0]
        if len(label) == 0:
            return Reason.INVALID_LABEL, rest
    if len(parts) >= 2:
        try:
            size = int(parts[1])
        except ValueError:
            return Reason.INVALID_SIZE, rest
    if len(parts) >= 3:
        tipe = parts[2]
        if len(tipe) != 1:
            return Reason.INVALID_TIPE, rest
        if not tipe.isalpha():
            return Reason.INVALID_TIPE, rest

    return Label(label, size, tipe), rest


def _read_value(adif: str, size: int) -> Tuple[str | Reason, str]:
    if adif == "" or len(adif) < size:
        return Reason.EOF, ""
    return par.read_n(adif, size)
