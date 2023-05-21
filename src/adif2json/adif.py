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
        if isinstance(field, ParseError) or isinstance(field, SegmentError):
            if field.reason == Reason.EOF:
                return Adif(headers, qsos, errors)
            elif field.reason == Reason.EOH:
                headers = current
                current = Record({})
            elif field.reason == Reason.EOR:
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
        else:
            print(emit)
            raise NotImplementedError

    last_line = 0
    last_column = 0
    state = par.State()
    for s in adif:
        state, emit = par.state_machine(state, s)
        if emit is not None:
            yield _par2reason(emit)
        last_line = s.line
        last_column = s.column

    # check final state
    state, emit = par.state_machine(
        state, par.Character(" ", last_line, last_column + 1)
    )
    if emit is not None:
        yield _par2reason(emit)
    if isinstance(state, par.State) or isinstance(state, par.Remainder):
        print("end of file")
    elif isinstance(state, par.Value):
        yield SegmentError(
            Reason.TRUNCATED_FILE,
            state.name[0].line,
            state.name[0].column,
            last_line,
            last_column,
        )
    else:
        print("state: ", state)
        yield ParseError(Reason.TRUNCATED_FILE, last_line, last_column)
