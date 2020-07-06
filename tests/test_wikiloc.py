import pytest

from wikiloc_cim_data import (
    get_routes_list,
    select_trekking_routes_from_list,
    get_title,
)

from bs4.element import Tag, ResultSet


def open_file(path):
    with open(path) as f:
        return f.read()


TEST_PAGE = open_file("./tests/testing_html_pages/wikiloc.html")
ROUTES_TAG = "div.main__results:nth-child(2)"
TITLE_TAG = open_file("./tests/testing_html_pages/title_tag.html")


def test_get_routes_list():
    """Test scrape route list from wikiloc cim search.

    WHEN: Wikiloc page is scraped
    THEN: Return only the list div
    """
    routes_list = get_routes_list(TEST_PAGE, ROUTES_TAG)

    assert isinstance(routes_list, Tag)


def test_select_trekking_routes_from_list():
    routes_list = get_routes_list(TEST_PAGE, ROUTES_TAG)
    lst = select_trekking_routes_from_list(routes_list)
    assert isinstance(lst, dict)


def test_get_title():
    pass
