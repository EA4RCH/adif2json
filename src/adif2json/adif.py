from functools import reduce
import adif2json.parser as par


import json
import logging
from typing import Iterable, Optional, Dict, List
from dataclasses import dataclass, asdict


def to_json_lines(adif: str) -> Iterable[str]:
    def _to_jsonline(d: Dict[str, str]) -> str:
        return f"{json.dumps(d)}\n"

    if adif == "":
        logging.warning("Empty ADIF")
        return ""
    logging.info(f"Converting {len(adif)} characters to dicts")
    dicts = to_dict(adif)
    logging.info("Converted to dicts")
    logging.info("Converting to JSON lines")
    yield from map(_to_jsonline, dicts)


def to_json(adif: str) -> str:
    if adif == "":
        logging.warning("Empty ADIF")
        return "{}"
    dicts = list(to_dict(adif))
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
    if not isinstance(record, Fields):
        logging.error(f"Unexpected record type {type(record)}")
        return record
    if isinstance(parsed, par.Field):
        logging.debug(f"Try to add field (Field+Field) {parsed.name}")
        if parsed.name in record.fields:
            logging.warning(f"Duplicate field {parsed.name}")
            error = par.FormatError("Duplicate field maybe eor missing", parsed.name)
            if not record.errors:
                record.errors = []
            record.errors.append(asdict(error))
        else:
            logging.debug(f"Adding field {parsed.name}")
            record.fields[parsed.name] = parsed.value
            if parsed.tipe:
                if not record.types:
                    record.types = {}
                record.types[parsed.name] = parsed.tipe
        return record
    elif isinstance(parsed, par.FormatError):
        logging.debug(f"Tyr to add error (Field+Error) {parsed.msg}")
        logging.error(f"Format error {parsed.msg}: '{parsed.part}'")
        if not record.errors:
            record.errors = []
        record.errors.append(asdict(parsed))
        return record
    elif isinstance(parsed, par.Eoh):
        logging.debug("Try to add EOH (Field+EOH)")
        if record.errors:
            return Record(record.fields, "headers", record.types, record.errors)
        else:
            return Record(record.fields, "headers", record.types)
    elif isinstance(parsed, par.Eor):
        logging.debug("Try to add EOR (Field+EOR)")
        if record.errors:
            return Record(record.fields, "qso", record.types, record.errors)
        else:
            return Record(record.fields, "qso", record.types)


def __create_records(
    acc: List[Record | Fields], field: Parsed
) -> List[Record | Fields]:
    logging.debug(f"Field to Record: {field}")
    if acc == []:
        logging.debug("Creating first Fields")
        acc = [Fields({}, {}, [])]
    if isinstance(acc[-1], Record):
        logging.debug("Detect Record, creating new Fields")
        acc.append(Fields({}, {}, []))
    if isinstance(acc[-1], Fields):
        logging.debug("Detect Fields, merging")
        acc[-1] = __merge(acc[-1], field)
    return acc


def _check_truncated(record: Record | Fields) -> Record:
    if isinstance(record, Record):
        return record
    if isinstance(record, Fields):
        logging.error("Truncated Record")
        rec = Record(record.fields, "qso", record.types)
        if record.errors:
            rec.errors = record.errors
        else:
            rec.errors = []
        error = par.FormatError("Truncated Record", "")
        rec.errors.append(asdict(error))
        return rec


def _to_dict(record: Record) -> Dict:
    return {
        "type": record.type,
        "fields": record.fields,
        "types": record.types,
        "errors": record.errors,
    }


def to_dict(adif: str) -> Iterable[Dict]:
    if adif == "":
        logging.warning("Empty ADIF")
        return
    fields = par.parse_all(adif)
    records = reduce(__create_records, fields, [])
    not_truncated = map(_check_truncated, records)
    dict_records = map(_to_dict, not_truncated)
    yield from dict_records
