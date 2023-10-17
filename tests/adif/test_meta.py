import json
import adif2json.adif as ad


def test_empty_meta():
    imp = [
        "<call:6>EA4HFF<EOR>",
    ]
    meta = {}

    adif = list(ad.to_json_lines(imp, meta))

    assert len(adif) == 1
    l = json.loads(adif[0])

    expected = {
        "call": "EA4HFF",
        "_meta": {
            "type": "qso"
        }
    }

    assert l == expected


def test_simple_meta():
    imp = [
        "<call:6>EA4HFF<EOR>",
    ]
    meta = {
        "source": "activation",
        "activator": "EA4HFF",
        "dme": "28079",
        "vertice": "VGM-001",
    }
    adif = list(ad.to_json_lines(imp, meta))

    assert len(adif) == 1
    l = json.loads(adif[0])

    expected = {
        "call": "EA4HFF",
        "_meta": {
            "type": "qso",
            "source": "activation",
            "activator": "EA4HFF",
            "dme": "28079",
            "vertice": "VGM-001",
        }
    }

    assert l == expected
