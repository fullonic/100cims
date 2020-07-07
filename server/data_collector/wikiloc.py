from dataclasses import dataclass
from typing import List

from selenium import webdriver

from .feec import CimsList
from .utils import _collect_wikiloc_data, accept_cookie, setup_browser


@dataclass
class WikiLoc:
    """Wikiloc data collector."""

    url: str

    def collect(self, driver: webdriver, cims_list: List):
        """Run collector script by order."""
        driver.get(self.url)
        accept_cookie(driver)
        return _collect_wikiloc_data(driver, cims_list)


if __name__ == "__main__":
    """Run standallone wikiloc browser collector.

    Mainly for testing
    """
    driver = setup_browser()
    cims_lst = CimsList.get_all()[:3]
    url = "https://es.wikiloc.com/"
    wikiloc = WikiLoc(url)
    wikiloc.collect(driver, cims_lst)
