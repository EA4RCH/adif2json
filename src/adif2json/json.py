import json


def to_adif(input_json: str) -> str:
    """
    Convert a json string to an adif string.
    """
    content = json.loads(input_json)
    adif_out = ""
    if "fields" in content:
        for label in content["fields"].keys():
            value = content["fields"][label]
            tipe = None
            if "types" in content and label in content["types"]:
                tipe = content["types"][label]
            if tipe:
                adif_out += f"<{label}:{len(value)}:{tipe}>{value}"
            else:
                adif_out += f"<{label}:{len(value)}>{value}"
    if "type" in content and content["type"] == "headers":
        adif_out += "<EOH>"
    else:
        adif_out += "<EOR>"
    return adif_out
