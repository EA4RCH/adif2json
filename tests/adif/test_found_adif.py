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

    res = to_dict(imp)

    assert isinstance(res, dict)
    assert "errors" not in res
