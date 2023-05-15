import adif2json.parser as par


from typing import Optional, Tuple, Dict, List
from dataclasses import dataclass, asdict


Reason = str


@dataclass
class Field:
    label: str
    tipe: Optional[str] = None
    value: Optional[str] = None


@dataclass
class Label:
    label: str
    size: Optional[int] = None
    tipe: Optional[str] = None


def to_json(adif: str) -> str:
    if adif == "": return '{"qsos": []}'

    #headers, rest = _read_headers(adif)
    return '{"qsos": []}'


def to_dict(adif: str) -> Dict:
    out = {}
    headers, rest = _read_headers(adif)
    if headers is None:
        return out
    if headers is not None:
        out["headers"] = [asdict(h) for h in headers]
    # TODO: read qsos
    return out


def _read_headers(adif: str) -> Tuple[List[Field] | None, str]:
    headers = []
    rest = adif

    while len(rest) > 0:
        field, rest = _read_field(rest)
        if not field:
            return headers, rest
        if isinstance(field, str):
            # TODO: handle reason
            continue
        if field.label == "eoh":
            # end of headers
            return headers, rest
        headers.append(field)
    return None, rest



def _read_field(adif: str) -> Tuple[Field | Reason | None, str]:
    label, rest =  _read_label(adif)
    if not label:
        return None, ""
    if isinstance(label, str):
        return label, rest
    if not label.size:
        return Field(label.label), rest
    if label.size and label.size > 0:
        maybe_value = _read_value(rest, label.size)
        if not maybe_value:
            return None, rest
        value, rest = maybe_value
        return Field(label.label, label.tipe, value), rest
    raise Exception("Unexpected")


def _read_label(adif: str) -> Tuple[Label | Reason | None, str]:
    rest = par.discard_forward(adif, '<')
    if not rest:
        return None, ""

    maybe_content = par.read_until(rest, '>')
    if not maybe_content:
        return None, ""

    content, rest = maybe_content
    if not content:
        return "Empty label", rest

    parts = content.split(':')
    rest = rest[1:]
    label = ""
    size = None
    tipe = None

    if len(parts) >= 1:
        label = parts[0].lower()
        if len(label) == 0:
            return "Empty label", rest
    if len(parts) >= 2:
        try:
            size = int(parts[1])
        except ValueError:
            return "Size is not a number", rest
    if len(parts) >= 3:
        tipe = parts[2].upper()
        if len(tipe) != 1:
            return "Type is not a single character", rest
        if not tipe.isalpha():
            return "Type is not a letter", rest

    return Label(label, size, tipe), rest


def _read_value(adif: str, size: int) -> Optional[Tuple[str, str]]:
    return par.read_n(adif, size)
