import adif2json.parser as par


import json
from enum import Enum
from typing import Iterator, Optional, Dict, List
from dataclasses import dataclass, asdict


@dataclass
class Record:
    fields: Dict[str, str]
    type: Optional[str] = None
    types: Optional[Dict[str, str]] = None
    errors: Optional[List[Dict[str, str]]] = None


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

    open_record = False
    for maybe_field in par.parse_fields(adif):
        if isinstance(maybe_field, par.ParseError):
            if not current.errors:
                current.errors = []
            current.errors.append(
                asdict(maybe_field, dict_factory=_custom_asdict_factory)
            )
            open_record = True
        elif maybe_field == par.Eoh():
            headers = current
            headers.type = "headers"
            yield headers
            open_record = False
            current = Record({})
        elif maybe_field == par.Eor():
            if current.errors and len(current.errors) > 0:
                current.type = "qso"
                yield current
            elif len(current.fields) > 0:
                current.type = "qso"
                yield current
            open_record = False
            current = Record({})
        elif isinstance(maybe_field, par.Field):
            current.fields[maybe_field.name] = maybe_field.value
            if maybe_field.tipe:
                if not current.types:
                    current.types = {}
                current.types[maybe_field.name] = maybe_field.tipe
            open_record = True
        else:
            print(f"not implemented: {type(maybe_field)} -> {maybe_field}")
            raise NotImplementedError

    if open_record:
        error = par.ParseError("Truncated Record", [])
        if not current.errors:
            current.errors = []
        current.errors.append(asdict(error, dict_factory=_custom_asdict_factory))

    if current.errors and len(current.errors) > 0:
        current.type = "qso"
        yield current
    elif len(current.fields) > 0:
        current.type = "qso"
        yield current
