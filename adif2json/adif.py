import adif2json.parser as par


import json
import logging
from typing import Iterable, Optional, Dict, List
from dataclasses import dataclass, asdict


def to_json_lines(
    adif: Iterable[str], meta: Optional[Dict[str, str]] = None
) -> Iterable[str]:
    """
    Convert an ADIF file to JSON lines, it's a generator that yields
    JSON lines. This will convert line by line, so it's memory efficient.
    """
    def _to_jsonline(d: Dict[str, str]) -> str:
        return f"{json.dumps(d)}\n"

    def _meta_addition(d: Dict) -> Dict:
        if meta:
            out = {**d}
            for k, v in meta.items():
                out["_meta"][k] = v
        return d

    if adif == "":
        logging.warning("Empty ADIF")
        return ""

    dicts = to_dict(adif)
    logging.info("Converted to dicts")
    logging.info("Converting to JSON lines")
    if meta:
        logging.info("Adding meta")
        dicts = map(_meta_addition, dicts)
    yield from map(_to_jsonline, dicts)


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


def _merge(record: Fields, parsed: Parsed) -> Fields | Record:
    """
    Merge a parsed field with a record. This function is used to create
    a record from a list of parsed fields.
    This will control if the parsed field is a Field, a FormatError, a
    EOH or a EOR.
    """
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


def _create_records(fields: Iterable[Parsed]) -> Iterable[Record | Fields]:
    """
    Create records from fields, it's a generator that yields
    records as they are created.

    It's a generator because it's more efficient than creating
    a list of records and then yielding them.
    """
    current = Fields({}, {}, [])
    for field in fields:
        logging.debug(f"Field: {field}")
        current = _merge(current, field)
        if isinstance(current, Record):
            yield current
            current = Fields({}, {}, [])
    if current.fields or current.errors:
        yield current


def _check_truncated(record: Record | Fields) -> Record:
    """
    Check if a record is truncated, if it is, it returns a
    Record with the error, if not, it returns the record.

    We can know if a record is truncated if it's a Fields
    object. Because if it's a Record, it means that it has
    been merged with an EOR, and if it's a Fields, it means
    that it hasn't been merged with an EOR.
    """
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
    """
    helper function to convert a record to a dictionary, it's a
    way faster than using asdict from dataclasses
    """
    meta = {
        "type": record.type,
    }
    if record.types:
        meta["types"] = record.types
    if record.errors:
        meta["errors"] = record.errors
    return {**record.fields, "_meta": meta}


def to_dict(adif: Iterable[str]) -> Iterable[Dict]:
    """
    Convert ADIF to a list of dictionaries, this is the
    main function of the module. It takes an iterable of
    ADIF lines and returns an iterable of dictionaries.
    """
    if adif == "":
        logging.warning("Empty ADIF")
        return
    fields = par.parse_all(adif)
    records = _create_records(fields)
    not_truncated = map(_check_truncated, records)
    dict_records = map(_to_dict, not_truncated)
    yield from dict_records
