import json

import pytest
import bs4
from feec_cim_data import (
    cims,
    get_essential_cim_list,
    list_to_dict,
    complementary_info,
)


def open_file(path):
    with open(path) as f:
        return f.read()


TAG_SCRIPT_TEST = open_file("./tests/testing_html_pages/tag.txt")
HTML_CIM_PAGE = open_file("./tests/testing_html_pages/cim_page.html")
ESSENTIAL_PATTERN = r"var cims_essencials = \[(.*?)\]"


@pytest.mark.vcr()
def test_scrape_cims_main_page():
    """Test scrape main page."""
    res = cims("https://www.feec.cat/activitats/100-cims/")
    assert isinstance(res, bs4.Tag)


def test_scrape_cims():
    """Test filter essential scripts from cims main page."""
    lst = get_essential_cim_list(ESSENTIAL_PATTERN, TAG_SCRIPT_TEST)
    assert isinstance(lst, list)


def test_dict_from_list():
    """Test convert a list of dictionary in string format to python native dict."""
    lst = [
        'nombre: "El Cogulló de Cabra",lat: "41.4290355033", lang: "1.30575794888", url: "https://www.feec.cat/activitats/100-cims/cim/el-cogullo-de-cabra/"',
        'nombre: "Puig de Tretzevents",lat: "42.492101894", lang: "2.4683643295", url: "https://www.feec.cat/activitats/100-cims/cim/puig-de-tretzevents/"',
        'nombre: "Torre de Madeloc",lat: "42.4904284262", lang: "3.07511682009", url: "https://www.feec.cat/activitats/100-cims/cim/torre-de-madeloc/"',
    ]
    dic = list_to_dict(lst)
    expected = {
        "nombre": "El Cogulló de Cabra",
        "lat": 41.4290355033,
        "lang": 1.30575794888,
        "url": "https://www.feec.cat/activitats/100-cims/cim/el-cogullo-de-cabra/",
    }
    assert expected == dic[0]
    assert isinstance(dic, list)
    assert isinstance(dic[0], dict)


@pytest.mark.vcr()
def test_complementary_info():
    cim_info = complementary_info(
        "https://www.feec.cat/activitats/100-cims/cim/la-mola/"
    )
    assert isinstance(cim_info, dict)
    expected = {
        "comarca": "Baix Penedès, Tarragonès",
        "altitude": 317,
        "img_url": "https://www.feec.cat/wp-content/uploads/2019/04/La-Mola-Bonastre-scaled.jpg",
    }
    assert cim_info == expected
