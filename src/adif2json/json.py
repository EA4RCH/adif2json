import json


def to_adif(input_json: str) -> str:
    """
    Convert a json string to an adif string.
    """
    if not input_json:
        return ""
    content = json.loads(input_json)
    adif_out = ""
    if "fields" in content:
        for label in content["fields"].keys():
            value = content["fields"][label]
            tipe = None
            if "types" in content and content["types"] and label in content["types"]:
                tipe = content["types"][label]
            if tipe:
                adif_out += f"<{label}:{len(value)}:{tipe}>{value}"
            else:
                adif_out += f"<{label}:{len(value)}>{value}"
    if adif_out and "type" in content and content["type"] == "headers":
        adif_out += "<EOH>"
    elif adif_out and "type" in content and content["type"] == "qso":
        adif_out += "<EOR>"
    return adif_out


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
