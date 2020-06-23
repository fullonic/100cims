from feec_cim_data import get_essential_cim_basic_information


def test_get_essential_cim_basic_information():
    cims = get_essential_cim_basic_information()
    cims_group = "essential repte".split(" ")
    expected_keys = "nombre lat lang url".split(" ")

    assert isinstance(cims, dict)
    assert isinstance(cims["essential"], list)
    assert list(cims["essential"][0].keys()) == expected_keys
    assert list(cims.keys()) == cims_group
    assert len(cims["essential"]) == 150
    assert len(cims["repte"]) == 158
