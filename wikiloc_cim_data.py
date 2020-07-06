import random
from time import sleep

import bs4
from bs4.element import Tag, ResultSet
from selenium import webdriver
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver.firefox.options import Options

#########################
# Helper functions
#########################
def _filter_by_html_tag(page: str, tag: str) -> bs4.element.Tag:
    soup = bs4.BeautifulSoup(page, features="html.parser")
    return soup.select(tag)[0]


def search_cim(driver: webdriver, keyword: str) -> None:
    """Wikiloc search box input."""
    cim_name = keyword
    search = driver.find_element_by_class_name("search-box__input")
    search.send_keys(cim_name)
    search.click()


def accept_cookie(driver: webdriver) -> None:
    """Wikiloc accept cookie policy."""
    btn = driver.find_element_by_id("acept-cookies")
    btn.click()


def get_routes_list(page, tag):
    """Get cim route list from wikiloc page."""
    return _filter_by_html_tag(page, tag)


def get_title(tag) -> str:
    _title = tag.select("div.trail-card__title-wrapper")[0].text
    title = _title.strip().replace("\n", " ")
    breakpoint()
    return title


def select_trekking_routes_from_list(routes_list: bs4.Tag):
    route_html_card = routes_list.select("div.trail")
    cards_list = routes_list.select("div.trail")
    card = cards_list[0]
    card_header = card.select("div.trail-card__header")[0]
    _title_tag = card_header.select("div:nth-child(2)")
    breakpoint()
    title = get_title(_title_tag[0])
    trekking_routes = None
    return trekking_routes


def main():
    # Add agent list
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
        "Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36",
        "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1",
    ]  # noqa

    user_agent = random.choice(user_agents)
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", user_agent)
    opts = Options()
    # opts.headless = True
    driver: webdriver = webdriver.Firefox(firefox_profile=profile, options=opts)
    cim_url = "https://es.wikiloc.com/"
    driver.get(cim_url)
    accept_cookie(driver)
    cims_list = ["El Cogulló de Cabra", "Puig de Tretzevents", "Torre de Madeloc"]

    sleep(0.5)
    for cim_name in cims_list:
        search_cim(driver, cim_name)
        try:
            btn_select_first = driver.find_element_by_class_name(
                "search-box-item__first"
            )
        except ElementClickInterceptedException:
            # handle posible error here
            print("ERROR")
        btn_select_first.click()

        page = driver.page_source

        # scrape list of routes
        get_routes_list(page)


if __name__ == "__main__":
    main()
