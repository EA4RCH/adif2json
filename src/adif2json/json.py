import json


def to_adif(input_json: str) -> str:
    """
    Convert a json string to an adif string.
    """
    content = json.loads(input_json)
    adif_out = ""
    if "headers" in content:
        headers = content["headers"]
        if "fields" in headers:
            for label in headers["fields"].keys():
                value = headers["fields"][label]
                tipe = None
                if "types" in headers and label in headers["types"]:
                    tipe = headers["types"][label]
                if tipe:
                    adif_out += f"<{label}:{len(value)}:{tipe}>{value}"
                else:
                    adif_out += f"<{label}:{len(value)}>{value}"
            adif_out += "<EOH>"
    if "qsos" in content:
        qsos = content["qsos"]
        for qso in qsos:
            for label in qso["fields"].keys() if "fields" in qso else []:
                value = qso["fields"][label]
                tipe = None
                if "types" in qso and label in qso["types"]:
                    tipe = qso["types"][label]
                if tipe:
                    adif_out += f"<{label}:{len(value)}:{tipe}>{value}"
                else:
                    adif_out += f"<{label}:{len(value)}>{value}"
            adif_out += "<EOR>"
    return adif_out
