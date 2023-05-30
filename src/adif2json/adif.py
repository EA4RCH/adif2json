from functools import reduce
import adif2json.parser as par


import json
from typing import Iterator, Optional, Dict, List
from dataclasses import dataclass, asdict


def to_json_lines(adif: Iterator[str] | str) -> Iterator[str]:
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


@dataclass
class Record:
    fields: Dict[str, str]
    type: str = "qso"
    types: Optional[Dict[str, str]] = None
    errors: Optional[List[Dict[str, str]]] = None
    open: bool = True


def to_dict(adif: str) -> List[Dict]:
    def _create_records(
        acc: List[Record], field: par.Field | par.FormatError | par.Eoh | par.Eor
    ) -> List[Record]:
        if acc == []:
            acc = [Record({})]
        rec = acc[-1]
        if isinstance(field, par.Field):
            rec.fields[field.name] = field.value
            if field.tipe:
                if not rec.types:
                    rec.types = {}
                rec.types[field.name] = field.tipe
        elif isinstance(field, par.FormatError):
            if not rec.errors:
                rec.errors = []
            rec.errors.append(asdict(field))
        elif isinstance(field, par.Eoh):
            rec.type = "headers"
            acc.append(Record({}))
        elif isinstance(field, par.Eor):
            rec.open = False
            acc.append(Record({}))

        return acc

    def _to_dict(record: Record) -> Dict:
        d = asdict(record)
        del d["open"]
        return d

    fields = par.parse_all(adif)

    records = list(reduce(_create_records, fields, [Record({})]))
    if len(records) > 0:
        if records[-1].fields == {} and records[-1].errors is None:
            records = records[:-1]
        elif records[-1].open:
            error = par.ParseError("Truncated Record", [])
            if not records[-1].errors:
                records[-1].errors = []
            records[-1].errors.append(asdict(error))
    return list(map(_to_dict, records))
