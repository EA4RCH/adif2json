from adif2json.adif import to_dict


def test_good_1():
    imp = [
        "<QSO_DATE:8>20230407",
        "<TIME_ON:6>072423",
        "<TIME_OFF:6>072423",
        "<STATION_CALLSIGN:8>EA5HUS/2",
        "<FREQ:6>3.5000",
        "<BAND:3>80M",
        "<CONTEST_ID:5>DXPED",
        "<MODE:3>SSB",
        "<CALL:6>EA4AVM",
        "<RST_SENT:2>59",
        "<RST_RCVD:2>59",
        "<APP_DXLOG_RCVD:0>",
        "<APP_DXLOG_RECINFO:0>",
        "<PFX:3>EA4",
        "<APP_DXLOG_POINTS:1>1",
        "<APP_DXLOG_STNID:4>STN1",
        "<APP_DXLOG_MULT1:0>",
        "<APP_DXLOG_MULT2:0>",
        "<APP_DXLOG_MULT3:0>",
        "<APP_DXLOG_STN:1>R",
        "<EOR>",
    ]

    res_l = list(to_dict(imp))

    assert len(res_l) == 1
    res = res_l[0]

    expected = {
        "QSO_DATE": "20230407",
        "TIME_ON": "072423",
        "TIME_OFF": "072423",
        "STATION_CALLSIGN": "EA5HUS/2",
        "FREQ": "3.5000",
        "BAND": "80M",
        "CONTEST_ID": "DXPED",
        "MODE": "SSB",
        "CALL": "EA4AVM",
        "RST_SENT": "59",
        "RST_RCVD": "59",
        "APP_DXLOG_RCVD": "",
        "APP_DXLOG_RECINFO": "",
        "PFX": "EA4",
        "APP_DXLOG_POINTS": "1",
        "APP_DXLOG_STNID": "STN1",
        "APP_DXLOG_MULT1": "",
        "APP_DXLOG_MULT2": "",
        "APP_DXLOG_MULT3": "",
        "APP_DXLOG_STN": "R",
        "_meta": {
            "type": "qso",
        }
    }

    assert res == expected
