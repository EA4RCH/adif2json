import adif2json.parser as par


import json
from enum import Enum
from typing import Any, Iterator, Optional, Dict, List
from dataclasses import dataclass, asdict
from functools import singledispatch


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

    @classmethod
    def tostring(cls, val):
        for k, v in vars(cls).iteritems():
            if v == val:
                return k


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
    type: Optional[str] = None
    types: Optional[Dict[str, str]] = None
    errors: Optional[List[Dict[str, str]]] = None


@dataclass
class Adif:
    headers: Optional[Record] = None
    qsos: Optional[List[Record]] = None
    errors: Optional[List[ParseError | SegmentError]] = None


def to_json_lines(adif: Iterator[str] | str) -> Iterator[str]:
    """
    Must return a json lines iterator.
    """
    if adif == "":
        return ""
    dicts = to_dict(adif)
    for d in dicts:
        yield f"{json.dumps(d)}\n"


def to_json(adif: Iterator[str] | str) -> Iterator[str]:
    if adif == "":
        yield "{}"
    dicts = to_dict(adif)
    first = True
    for d in dicts:
        if first:
            first = False
            yield "["
        yield f"{json.dumps(d)},"
    if not first:
        yield "]"


def _custom_asdict_factory(data):
    def convert_value(obj):
        if isinstance(obj, Enum):
            return obj.name
        return obj

    return dict((k, convert_value(v)) for k, v in data)


def to_dict(adif: Iterator[str] | str) -> Iterator[Dict]:
    records = _read_fields(par.stream_character(adif))

    for record in records:
        record_dict = asdict(record, dict_factory=_custom_asdict_factory)
        yield record_dict


def _read_fields(adif: Iterator[par.Character]) -> Iterator[Record]:
    headers: Optional[Record] = None
    current: Record = Record({})

    for maybe_field in _read_field(adif):
        if isinstance(maybe_field, ParseError) or isinstance(maybe_field, SegmentError):
            if not current.errors:
                current.errors = []
            current.errors.append(
                asdict(maybe_field, dict_factory=_custom_asdict_factory)
            )
            continue
        elif maybe_field == Reason.EOH:
            headers = current
            headers.type = "headers"
            yield headers
            current = Record({})
        elif maybe_field == Reason.EOR:
            if current.errors and len(current.errors) > 0:
                current.type = "qso"
                yield current
            elif len(current.fields) > 0:
                current.type = "qso"
                yield current
            current = Record({})
        elif isinstance(maybe_field, Field):
            current.fields[maybe_field.label] = maybe_field.value
            if maybe_field.tipe:
                if not current.types:
                    current.types = {}
                current.types[maybe_field.label] = maybe_field.tipe
    if current.errors and len(current.errors) > 0:
        current.type = "qso"
        yield current
    elif len(current.fields) > 0:
        current.type = "qso"
        yield current


Field_reason = Field | ParseError | SegmentError | Reason


@singledispatch
def _par2reason(x: Any) -> Any:
    print(f"not par2reason implemented: {type(x)}")
    raise NotImplementedError


@_par2reason.register
def _(emit: par.Value) -> Field_reason:
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


@_par2reason.register
def _(_: par.Eoh) -> Field_reason:
    return Reason.EOH


@_par2reason.register
def _(_: par.Eor) -> Field_reason:
    return Reason.EOR


@_par2reason.register
def _(emit: par.IvalidLabel) -> Field_reason:
    return ParseError(Reason.INVALID_LABEL, emit.name[0].line, emit.name[0].column)


@_par2reason.register
def _(emit: par.ExceededValue) -> Field_reason:
    return SegmentError(
        Reason.EXCEEDENT_VALUE,
        emit.remainder[0].line,
        emit.remainder[0].column,
        emit.remainder[-1].line,
        emit.remainder[-1].column,
    )


@_par2reason.register
def _(emit: par.IvalidLabelSize) -> Field_reason:
    return SegmentError(
        Reason.INVALID_SIZE,
        emit.size[0].line,
        emit.size[0].column,
        emit.size[-1].line,
        emit.size[-1].column,
    )


@_par2reason.register
def _(emit: par.IvalidLabelTipe) -> Field_reason:
    if not emit.tipe:
        raise Exception("Invalid type emit")
    return ParseError(
        Reason.INVALID_TIPE,
        emit.tipe.line,
        emit.tipe.column,
    )


@_par2reason.register
def _(emit: par.TruncatedValue) -> Field_reason:
    return ParseError(
        Reason.INVALID_TIPE,
        emit.value[-1].line,
        emit.value[-1].column,
    )


def _read_field(adif: Iterator[par.Character]) -> Iterator[Field_reason]:
    state = par.State()
    for emit in par.state_machine(state, adif):
        if emit is not None:
            yield _par2reason(emit)
        # TODO: last line and column
        # last_line = s.line
        # last_column = s.column

    """
    TODO: fix this
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
    """
