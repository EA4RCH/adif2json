import json

def to_adif(input_json: str) -> str:
    """
    Convert a json string to an adif string.
    """
    content = json.loads(input_json)
    adif_out = ""
    if "headers" in content:
        if "fields" in content["headers"]:
            for label in content["headers"]["fields"].keys():
                value = content["headers"]["fields"][label]
                tipe = None
                if "types" in content["headers"] and label in content["headers"]["types"]:
                    tipe = content["headers"]["types"][label]
                if tipe:
                    adif_out += "<{}:{}:{}>{}".format(label, len(str(value)), tipe, value)
                else:
                    adif_out += "<{}:{}>{}".format(label, len(str(value)), value)
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
                    adif_out += "<{}:{}:{}>{}".format(label, len(str(value)), tipe, value)
                else:
                    adif_out += "<{}:{}>{}".format(label, len(str(value)), value)
            adif_out += "<EOR>"
    return adif_out
