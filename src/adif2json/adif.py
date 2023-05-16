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
    EXCEEDENT_VALUE = 8


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
    types: Optional[Dict[str, str]] = None


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
            h = {}
            if adif_f.headers.types:
                h["types"] = adif_f.headers.types
            h["fields"] = adif_f.headers.fields
            out["headers"] = h
        else:
            out["headers"] = None
    if adif_f.qsos:
        qsos = []
        [asdict(qso) for qso in adif_f.qsos]
        for r in adif_f.qsos:
            q = {}
            if r.types:
                q["types"] = r.types
            q["fields"] = r.fields
            qsos.append(q)
        out["qsos"] = qsos
    if adif_f.errors:
        out["errors"] = [error.name for error in adif_f.errors]
    return out


def _read_fields(adif: par.Position) -> Adif:
    if adif.remaining == "": return Adif()
    current : Record = Record({})
    headers : Optional[Record] = None
    qsos = []
    errors = []
    rest = adif

    while True:
        if isinstance(rest, par.EndOfFile):
            return Adif(errors=[Reason.EOF])
        field, rest = _read_field(rest)
        if isinstance(field, Reason):
            if field == Reason.EOF:
                return Adif(headers, qsos, errors)
            elif field == Reason.EOH:
                headers = current
                current = Record({})
            elif field == Reason.EOR:
                if len(current.fields) > 0:
                    qsos.append(current)
                current = Record({})
            else:
                errors.append(field)
            continue

        current.fields[field.label] = field.value
        if field.tipe:
            if not current.types:
                current.types = {}
            current.types[field.label] = field.tipe
    raise Exception("Unexpected")


def _read_field(adif: par.Position) -> Tuple[Field | Reason, par.Position | par.EndOfFile]:
    label, rest =  _read_label(adif)
    if isinstance(label, Reason):
        return label, rest
    if not label.size or label.size < 1:
        if label.label.upper() == "EOH":
            return Reason.EOH, rest
        if label.label.upper() == "EOR":
            return Reason.EOR, rest
        return Reason.INVALID_SIZE, rest

    if isinstance(rest, par.EndOfFile):
        return Reason.EOF, rest

    value, rest = par.read_n(rest, label.size)
    if isinstance(value, Reason):
        return value, rest
    if label.tipe:
        field = Field(label.label, value, label.tipe)
    else:
        field = Field(label.label, value)

    if isinstance(rest, par.EndOfFile):
        return Reason.EOF, rest

    rr = par.read_until(rest, '<')
    if not rr:
        return field, rest
    remaining, rest = rr
    if remaining.strip() != "":
        return Reason.EXCEEDENT_VALUE, rest
    return field, rest


def _read_label(adif: par.Position) -> Tuple[Label | Reason, par.Position | par.EndOfFile]:
    rest = par.discard_forward(adif, '<')
    if isinstance(rest, par.EndOfFile):
        return Reason.EOF, rest

    content, rest = par.read_until(rest, '>')
    if content == "":
        return Reason.INVALID_LABEL, rest
    if isinstance(rest, par.EndOfFile):
        return Reason.EOF, rest

    parts = content.split(':')
    rest = par.discard_n(rest, 1)
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
