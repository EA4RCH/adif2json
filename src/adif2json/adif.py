from functools import reduce
import adif2json.parser as par


import json
import logging
from typing import Optional, Dict, List
from dataclasses import dataclass, asdict


def to_json_lines(adif: str) -> str:
    if adif == "":
        logging.warning("Empty ADIF")
        return ""
    logging.info(f"Converting {len(adif)} characters to JSONL")
    dicts = to_dict(adif)
    logging.info(f"Converting {len(dicts)} records to JSONL")
    out = ""
    for d in dicts:
        out += f"{json.dumps(d)}\n"
    return out


def to_json(adif: str) -> str:
    if adif == "":
        logging.warning("Empty ADIF")
        yield "{}"
    dicts = to_dict(adif)
    logging.info(f"Converting {len(dicts)} records to JSON")
    return f"{json.dumps(dicts)}"


@dataclass
class Record:
    fields: Dict[str, str]
    type: str = "qso"
    types: Optional[Dict[str, str]] = None
    errors: Optional[List[Dict[str, str]]] = None
    open: bool = True


def __create_records(
    acc: List[Record], field: par.Field | par.FormatError | par.Eoh | par.Eor
) -> List[Record]:
    if acc == []:
        acc = [Record({})]
    rec = acc[-1]
    if isinstance(field, par.Field):
        # TODO: Check if we are overwriting a field
        # maybe there is no eor
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


def to_dict(adif: str) -> List[Dict]:
    def _to_dict(record: Record) -> Dict:
        d = asdict(record)
        del d["open"]
        return d

    logging.info(f"Converting {len(adif)} characters to List dict")
    fields = par.parse_all(adif)
    logging.info(f"Readed {len(fields)} fields from ADIF")

    records = list(reduce(__create_records, fields, [Record({})]))
    logging.info(f"Created {len(records)} records from ADIF")

    if len(records) > 0:
        if records[-1].fields == {} and records[-1].errors is None:
            logging.warning("Empty last Record")
            records = records[:-1]
        elif records[-1].open:
            logging.error("Truncated Record")
            error = par.ParseError("Truncated Record", [])
            if not records[-1].errors:
                records[-1].errors = []
            records[-1].errors.append(asdict(error))
    return list(map(_to_dict, records))
