import adif2json.parser as par


def test_expected_finder():
    TEST_LINE = """
    <QSO_DATE:8>20230407 <TIME_ON:6>061156 <TIME_OFF:6>061156 <STATION_CALLSIGN:8>EA5HUS/2 <FREQ:6>3.5000 <BAND:3>80M <CONTEST_ID:5>DXPED <MODE:3>SSB <CALL:6>EA2DDE <RST_SENT:2>59 <RST_RCVD:2>59 <APP_DXLOG_RCVD:0> <APP_DXLOG_RECINFO:0> <PFX:3>EA2 <APP_DXLOG_POINTS:1>1 <APP_DXLOG_STNID:4>STN1 <APP_DXLOG_MULT1:2>EA <APP_DXLOG_MULT2:0> <APP_DXLOG_MULT3:0> <APP_DXLOG_STN:1>R <EOR>
    """
    res = list(par._iter_finder(TEST_LINE))

    expected = [
        ("QSO_DATE:8", "20230407 "),
        ("TIME_ON:6", "061156 "),
        ("TIME_OFF:6", "061156 "),
        ("STATION_CALLSIGN:8", "EA5HUS/2 "),
        ("FREQ:6", "3.5000 "),
        ("BAND:3", "80M "),
        ("CONTEST_ID:5", "DXPED "),
        ("MODE:3", "SSB "),
        ("CALL:6", "EA2DDE "),
        ("RST_SENT:2", "59 "),
        ("RST_RCVD:2", "59 "),
        ("APP_DXLOG_RCVD:0", " "),
        ("APP_DXLOG_RECINFO:0", " "),
        ("PFX:3", "EA2 "),
        ("APP_DXLOG_POINTS:1", "1 "),
        ("APP_DXLOG_STNID:4", "STN1 "),
        ("APP_DXLOG_MULT1:2", "EA "),
        ("APP_DXLOG_MULT2:0", " "),
        ("APP_DXLOG_MULT3:0", " "),
        ("APP_DXLOG_STN:1", "R "),
        ("EOR", "\n    "),
    ]

    assert res == expected


def test_small_line_bad_label():
    imput = "<call:6>EA4HFF<EOR><call:5>EA4AW<EOR><:4>EC5A<EOR>"
    res = list(par._iter_finder(imput))

    expected = [
        ("call:6", "EA4HFF"),
        ("EOR", ""),
        ("call:5", "EA4AW"),
        ("EOR", ""),
        (":4", "EC5A"),
        ("EOR", ""),
    ]

    assert res == expected


def test_small_line_ok():
    imput = "<call:6>EA4HFF<EOR><call:5>EA4AW<EOR><call:4>EC5A<EOR>"
    res = list(par._iter_finder(imput))

    expected = [
        ("call:6", "EA4HFF"),
        ("EOR", ""),
        ("call:5", "EA4AW"),
        ("EOR", ""),
        ("call:4", "EC5A"),
        ("EOR", ""),
    ]

    assert res == expected
