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
    TRUNCATED_FILE = 9


@dataclass
class ParseError:
    reason: Reason
    line: int
    column: int


@dataclass
class SegmentError:
    reason: Reason
    line: int
    column: int
    size: int


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
    errors: Optional[List[ParseError | SegmentError]] = None


def to_json(adif: str) -> str:
    if adif == "":
        return '{"qsos": []}'
    d = to_dict(adif)
    return json.dumps(d)


def to_dict(adif: str) -> Dict:
    adif_f = _read_fields(par.Position(adif))
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
        out["errors"] = [
            {"reason": e.reason.name, "line": e.line, "column": e.column}
            for e in adif_f.errors
            if isinstance(e, ParseError)
        ] + [
            {
                "reason": e.reason.name,
                "line": e.line,
                "column": e.column,
                "size": e.size,
            }
            for e in adif_f.errors
            if isinstance(e, SegmentError)
        ]
    return out


def _read_fields(adif: par.Position) -> Adif:
    if adif.remaining == "":
        return Adif()
    current: Record = Record({})
    headers: Optional[Record] = None
    qsos = None
    errors = None
    rest = adif

    while True:
        if isinstance(rest, par.EndOfFile):
            err = ParseError(Reason.TRUNCATED_FILE, rest.line, rest.column)
            return Adif(headers, qsos, errors=[err])
        field, rest = _read_field(rest)
        if isinstance(field, Reason) or isinstance(field, SegmentError):
            if isinstance(field, SegmentError):
                if not errors:
                    errors = []
                errors.append(field)
            elif field == Reason.EOF:
                return Adif(headers, qsos, errors)
            elif field == Reason.EOH:
                headers = current
                current = Record({})
            elif field == Reason.EOR:
                if len(current.fields) > 0:
                    if not qsos:
                        qsos = []
                    qsos.append(current)
                current = Record({})
            else:
                if not errors:
                    errors = []
                errors.append(field)
            continue

        current.fields[field.label] = field.value
        if field.tipe:
            if not current.types:
                current.types = {}
            current.types[field.label] = field.tipe


Field_reason = Tuple[Field | Reason | SegmentError, par.Position | par.EndOfFile]


def _read_field(adif: par.Position) -> Field_reason:
    label, rest = _read_label(adif)
    if isinstance(label, Reason) or isinstance(label, SegmentError):
        return label, rest
    if not label.size or label.size < 1:
        if label.label.upper() == "EOH":
            return Reason.EOH, rest
        if label.label.upper() == "EOR":
            return Reason.EOR, rest
        return Reason.INVALID_SIZE, rest

    if isinstance(rest, par.EndOfFile) or rest.remaining == "":
        return Reason.TRUNCATED_FILE, rest

    value, rest = par.read_n(rest, label.size)
    if label.tipe:
        field = Field(label.label, value, label.tipe)
    else:
        field = Field(label.label, value)

    if isinstance(rest, par.EndOfFile):
        return Reason.EOF, rest

    remaining, rest = par.read_until(rest, "<")
    if remaining.strip() != "":
        return Reason.EXCEEDENT_VALUE, rest
    return field, rest


Label_reason = Tuple[Label | Reason | SegmentError, par.Position | par.EndOfFile]


def _read_label(adif: par.Position) -> Label_reason:
    rest = par.discard_forward(adif, "<")
    label_start_line, label_start_column = rest.line, rest.column
    if isinstance(rest, par.EndOfFile):
        return Reason.EOF, rest

    content, rest = par.read_until(rest, ">")
    if content == "":
        return Reason.INVALID_LABEL, rest
    if isinstance(rest, par.EndOfFile):
        return Reason.EOF, rest

    parts = content.split(":")
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
            size_start_line, size_start_column = par._update_position(
                ":".join(parts[:1]), label_start_line, label_start_column
            )
            err = SegmentError(
                Reason.INVALID_SIZE, size_start_line, size_start_column, len(parts[1])
            )
            return err, rest
    if len(parts) >= 3:
        tipe = parts[2]
        if len(tipe) != 1:
            return Reason.INVALID_TIPE, rest
        if not tipe.isalpha():
            return Reason.INVALID_TIPE, rest

    return Label(label, size, tipe), rest
