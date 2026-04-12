import json
from typing import Iterable


def to_adif(input_json: str) -> str:
    """
    Convert a json string to an adif string.
    """
    if not input_json:
        return ""
    content = json.loads(input_json)
    adif_out = ""
    if len(content) > 1:
        types = content.get("_types")
        if not isinstance(types, dict):
            types = {}
        for label in content.keys():
            if label.startswith("_"):
                continue
            value = content[label]
            if label in types:
                tipe = types[label]
                adif_out += f"<{label}:{len(value)}:{tipe}>{value}"
            else:
                adif_out += f"<{label}:{len(value)}>{value}"
    record_type = content.get("_type")
    if adif_out and record_type == "headers":
        adif_out += "<EOH>"
    elif adif_out and record_type == "qso":
        adif_out += "<EOR>"
    return adif_out


def from_json_generator(jsgen: Iterable[str]) -> Iterable[str]:
    """
    Convert a json generator to an adif generator.
    """
    for line in jsgen:
        s = to_adif(line)
        s += "\n"
        yield s


def from_json_lines(jsonlines: str) -> str:
    """
    Convert a jsonlines string to an iterator of json objects.
    """
    out = ""
    for line in jsonlines.split("\n"):
        line = line.strip()
        if line:
            out += to_adif(line)
    return out
