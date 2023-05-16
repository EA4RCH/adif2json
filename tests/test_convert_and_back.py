import adif2json.adif as ad
import adif2json.json as js

import json
from hypothesis import given
import hypothesis.strategies as st

# Typical QSO fields
qso_fields = {
    "CALL": st.text(min_size=1),
    "QSO_DATE": st.text(min_size=8, max_size=8),
    "TIME_ON": st.text(min_size=4, max_size=4),
    "BAND": st.text(min_size=1),
    "MODE": st.text(min_size=1),
    "RST_SENT": st.text(min_size=1),
    "RST_RCVD": st.text(min_size=1),
    "NAME": st.text(min_size=1),
    "QTH": st.text(min_size=1),
}
type_char_strategy = st.characters(min_codepoint=ord('a'), max_codepoint=ord('z'))

type_fields = {
    "CALL": st.one_of(type_char_strategy, st.none()),
    "QSO_DATE": st.one_of(type_char_strategy, st.none()),
    "TIME_ON": st.one_of(type_char_strategy, st.none()),
    "BAND":  st.one_of(type_char_strategy, st.none()),
    "MODE": st.one_of(type_char_strategy, st.none()),
    "RST_SENT": st.one_of(type_char_strategy, st.none()),
    "RST_RCVD": st.one_of(type_char_strategy, st.none()),
    "NAME": st.one_of(type_char_strategy, st.none()),
    "QTH": st.one_of(type_char_strategy, st.none()),
}
qso_strategy = st.fixed_dictionaries(qso_fields)
type_strategy = st.fixed_dictionaries(type_fields)
json_strategy = st.fixed_dictionaries({"qsos": st.lists(st.fixed_dictionaries({"fields": qso_strategy, "types": type_strategy}))})

@given(json_strategy)
def test_adif_to_json_conversion(input_dict):
    gen_adif = js.to_adif(json.dumps(input_dict))
    gen_json = ad.to_json(gen_adif)
    output_dict = json.loads(gen_json)
    if input_dict != output_dict:
        print("==="*10)
        print(input_dict)
        print("---"*10)
        print(output_dict)
        print("==="*10)
    assert input_dict == output_dict
