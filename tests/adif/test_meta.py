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
    assert "fields" in l
    f = l["fields"]
    assert "call" in f
    assert f["call"] == "EA4HFF"
    assert "_meta" not in l


def test_simple_meta():
    imp = [
        "<call:6>EA4HFF<EOR>",
    ]
    meta = {
        "type": "activation",
        "activator": "EA4HFF",
        "dme": "28079",
        "vertice": "VGM-001",
    }
    adif = list(ad.to_json_lines(imp, meta))

    assert len(adif) == 1
    l = json.loads(adif[0])
    assert "fields" in l
    f = l["fields"]
    assert "call" in f
    assert f["call"] == "EA4HFF"
    assert "_meta" in l
    assert l["_meta"] == {
        "type": "activation",
        "activator": "EA4HFF",
        "dme": "28079",
        "vertice": "VGM-001",
    }
