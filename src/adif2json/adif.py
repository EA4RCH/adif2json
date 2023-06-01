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
class Fields:
    fields: Dict[str, str]
    types: Dict[str, str]
    errors: List[Dict[str, str]]


@dataclass
class Record:
    fields: Dict[str, str]
    type: str = "qso"
    types: Optional[Dict[str, str]] = None
    errors: Optional[List[Dict[str, str]]] = None


Parsed = par.Field | par.FormatError | par.Eoh | par.Eor


def __merge(record: Fields, parsed: Parsed) -> Fields | Record:
    if isinstance(parsed, par.Field):
        if parsed.name in record.fields:
            logging.warning(f"Duplicate field {parsed.name}")
            error = par.FormatError("Duplicate field maybe eor missing", parsed.name)
            if not record.errors:
                record.errors = []
            record.errors.append(asdict(error))
        else:
            record.fields[parsed.name] = parsed.value
            if parsed.tipe:
                if not record.types:
                    record.types = {}
                record.types[parsed.name] = parsed.tipe
        return record
    elif isinstance(parsed, par.FormatError):
        if not record.errors:
            record.errors = []
        record.errors.append(asdict(parsed))
        return record
    elif isinstance(parsed, par.Eoh):
        if record.errors:
            return Record(record.fields, "headers", record.types, record.errors)
        else:
            return Record(record.fields, "headers", record.types)
    elif isinstance(parsed, par.Eor):
        if record.errors:
            return Record(record.fields, "qso", record.types, record.errors)
        else:
            return Record(record.fields, "qso", record.types)


def __create_records(
    acc: List[Record | Fields], field: Parsed
) -> List[Record | Fields]:
    if acc == []:
        acc = [Fields({}, {}, [])]
    if isinstance(acc[-1], Record):
        acc.append(Fields({}, {}, []))
    acc[-1] = __merge(acc[-1], field)
    return acc


def to_dict(adif: str) -> List[Dict]:
    def _to_dict(record: Record) -> Dict:
        return {
            "type": record.type,
            "fields": record.fields,
            "types": record.types,
            "errors": record.errors,
        }

    logging.info(f"Converting {len(adif)} characters to List dict")
    fields = par.parse_all(adif)
    logging.info(f"Readed {len(fields)} fields from ADIF")

    records = list(reduce(__create_records, fields, []))
    logging.info(f"Created {len(records)} records from ADIF")

    if len(records) > 0:
        if isinstance(records[-1], Fields):
            logging.error("Truncated Record")
            rec = Record(records[-1].fields, "qso", records[-1].types)
            if records[-1].errors:
                rec.errors = records[-1].errors
            else:
                rec.errors = []
            error = par.FormatError("Truncated Record", "")
            rec.errors.append(asdict(error))
            records[-1] = rec
    return list(map(_to_dict, records))
