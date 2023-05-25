from adif2json.adif import to_dict


def test_good_1():
    imp = """
    <QSO_DATE:8>20230407
    <TIME_ON:6>072423
    <TIME_OFF:6>072423
    <STATION_CALLSIGN:8>EA5HUS/2
    <FREQ:6>3.5000
    <BAND:3>80M
    <CONTEST_ID:5>DXPED
    <MODE:3>SSB
    <CALL:6>EA4AVM
    <RST_SENT:2>59
    <RST_RCVD:2>59
    <APP_DXLOG_RCVD:0>
    <APP_DXLOG_RECINFO:0>
    <PFX:3>EA4
    <APP_DXLOG_POINTS:1>1
    <APP_DXLOG_STNID:4>STN1
    <APP_DXLOG_MULT1:0>
    <APP_DXLOG_MULT2:0>
    <APP_DXLOG_MULT3:0>
    <APP_DXLOG_STN:1>R
    <EOR>
    """

    res_l = list(to_dict(imp))

    assert len(res_l) == 1
    res = res_l[0]
    assert res["type"] == "qso"
    assert len(res["fields"]) == 20
    assert res["fields"]["QSO_DATE"] == "20230407"
    assert res["fields"]["TIME_ON"] == "072423"
    assert res["fields"]["TIME_OFF"] == "072423"
    assert res["fields"]["STATION_CALLSIGN"] == "EA5HUS/2"
    assert res["fields"]["FREQ"] == "3.5000"
    assert res["fields"]["BAND"] == "80M"
    assert res["fields"]["CONTEST_ID"] == "DXPED"
    assert res["fields"]["MODE"] == "SSB"
    assert res["fields"]["CALL"] == "EA4AVM"
    assert res["fields"]["RST_SENT"] == "59"
    assert res["fields"]["RST_RCVD"] == "59"
    assert res["fields"]["APP_DXLOG_RCVD"] == ""
    assert res["fields"]["APP_DXLOG_RECINFO"] == ""
    assert res["fields"]["PFX"] == "EA4"
    assert res["fields"]["APP_DXLOG_POINTS"] == "1"
    assert res["fields"]["APP_DXLOG_STNID"] == "STN1"
    assert res["fields"]["APP_DXLOG_MULT1"] == ""
    assert res["fields"]["APP_DXLOG_MULT2"] == ""
    assert res["fields"]["APP_DXLOG_MULT3"] == ""
    assert res["fields"]["APP_DXLOG_STN"] == "R"
    assert res["errors"] is None
