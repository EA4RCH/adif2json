import json

def to_adif(input_json: str) -> str:
    """
    Convert a json string to an adif string.
    """
    content = json.loads(input_json)
    if "qsos" in content:
        qsos = content["qsos"]
        adif_out = ""
        for qso in qsos:
            for key, value in qso.items():
                adif_out += "<{}:{}>{}, ".format(key.upper(), len(str(value)), value)
                adif_out = adif_out.rstrip(', ')
        adif_out += "<EOR>\n"
        return adif_out
    return ""
