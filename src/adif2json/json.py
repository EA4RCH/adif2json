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
            for label in qso["fields"].keys() if "fields" in qso else []:
                value = qso["fields"][label]
                tipe = None
                if "types" in qso and label in qso["types"]:
                    tipe = qso["types"][label]
                if tipe:
                    adif_out += "<{}:{}:{}>{} ".format(label, len(str(value)), tipe, value)
                else:
                    adif_out += "<{}:{}>{} ".format(label, len(str(value)), value)
            adif_out += "<EOR>\n"
        return adif_out
    return ""
