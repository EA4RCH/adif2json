import adif2json.parser as par


import json
from enum import Enum
from typing import Iterator, Optional, Dict, List
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
    start_line: int
    start_column: int
    end_line: int
    end_column: int


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


def to_dict(adif: Iterator[str] | str) -> Dict:
    adif_f = _read_fields(par.stream_character(adif))
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
                "start_line": e.start_line,
                "start_column": e.start_column,
                "end_line": e.end_line,
                "end_column": e.end_column,
            }
            for e in adif_f.errors
            if isinstance(e, SegmentError)
        ]
    return out


def _read_fields(adif: Iterator[par.Character]) -> Adif:
    current: Record = Record({})
    headers: Optional[Record] = None
    qsos = None
    errors = None

    for maybe_field in _read_field(adif):
        if isinstance(maybe_field, ParseError) or isinstance(maybe_field, SegmentError):
            if not errors:
                errors = []
            errors.append(maybe_field)
            continue
        elif maybe_field == Reason.EOH:
            headers = current
            current = Record({})
        elif maybe_field == Reason.EOR:
            if len(current.fields) > 0:
                if not qsos:
                    qsos = []
                qsos.append(current)
            current = Record({})
        elif isinstance(maybe_field, Field):
            current.fields[maybe_field.label] = maybe_field.value
            if maybe_field.tipe:
                if not current.types:
                    current.types = {}
                current.types[maybe_field.label] = maybe_field.tipe
    # TODO: check if there is qso ongoing to return a truncated file error
    if len(current.fields) > 0:
        if not qsos:
            qsos = []
        qsos.append(current)
    return Adif(headers, qsos, errors)


Field_reason = Field | ParseError | SegmentError | Reason


def _read_field(adif: Iterator[par.Character]) -> Iterator[Field_reason]:
    def _par2reason(emit: par.EmitState) -> Field_reason:
        if isinstance(emit, par.Value):
            if emit.tipe:
                field = Field(
                    par.charlist_to_str(emit.name),
                    par.charlist_to_str(emit.value),
                    emit.tipe.character,
                )
            else:
                field = Field(
                    par.charlist_to_str(emit.name),
                    par.charlist_to_str(emit.value),
                )
            return field
        elif isinstance(emit, par.Eoh):
            return Reason.EOH
        elif isinstance(emit, par.Eor):
            return Reason.EOR
        elif isinstance(emit, par.IvalidLabel):
            return ParseError(
                Reason.INVALID_LABEL, emit.name[0].line, emit.name[0].column
            )
        elif isinstance(emit, par.ExceededValue):
            return SegmentError(
                Reason.EXCEEDENT_VALUE,
                emit.remainder[0].line,
                emit.remainder[0].column,
                emit.remainder[-1].line,
                emit.remainder[-1].column,
            )
        elif isinstance(emit, par.IvalidLabelSize):
            return SegmentError(
                Reason.INVALID_SIZE,
                emit.size[0].line,
                emit.size[0].column,
                emit.size[-1].line,
                emit.size[-1].column,
            )
        elif isinstance(emit, par.IvalidLabelTipe):
            if not emit.tipe:
                raise NotImplementedError
            return ParseError(
                Reason.INVALID_TIPE,
                emit.tipe.line,
                emit.tipe.column,
            )
        else:
            print(emit)
            raise NotImplementedError

    last_line = 0
    last_column = 0
    state = par.State()
    record_open = False
    for s in adif:
        state, emit = par.state_machine(state, s)
        if emit is not None:
            em = _par2reason(emit)
            if isinstance(em, Field):
                record_open = True
            elif em == Reason.EOR:
                record_open = False
            elif em == Reason.EOH:
                record_open = False
            yield em
        last_line = s.line
        last_column = s.column

    state, emit = par.state_machine(
        state, par.Character(" ", last_line, last_column + 1)
    )
    if emit is not None:
        em = _par2reason(emit)
        if isinstance(em, Field):
            record_open = True
        elif em == Reason.EOR:
            record_open = False
        elif em == Reason.EOH:
            record_open = False
        yield em

    if record_open:
        yield ParseError(Reason.TRUNCATED_FILE, last_line, last_column)
    if isinstance(state, par.Value):
        yield SegmentError(
            Reason.TRUNCATED_FILE,
            state.name[0].line,
            state.name[0].column,
            last_line,
            last_column,
        )
        return
