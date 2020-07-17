from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import List
from queue import Queue
from selenium import webdriver
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
)
from .feec import CimsList
from .utils import (
    accept_cookie,
    setup_browser,
    search_cim,
    get_cim_routes_list,
    create_queue,
    run_multiple,
    ROUTES_TAG,
)


import asyncio


@dataclass
class WikiLoc:
    """Wikiloc data collector."""

    url: str
    search_urls: List = field(default_factory=list)
    routes_list: List = field(default_factory=list)

    def collect(self, driver: webdriver, cims_list: List):
        """Run collector script by order."""
        driver.get(self.url)
        accept_cookie(driver)

        for cim in cims_list:
            if search_cim(driver, cim["nombre"]):
                page = driver.page_source
                # scrape list of routes
                self.routes_list.append(
                    get_cim_routes_list(cim["uuid"], page, ROUTES_TAG)
                )
                # breakpoint()
                self.search_urls.append({cim["uuid"]: driver.current_url})
        return {"routes": self.routes_list, "search_urls": self.search_urls}


def _loop(workers: int = 4, debug: bool = False) -> asyncio.Event:
    loop = asyncio.get_event_loop()
    loop.set_default_executor(ThreadPoolExecutor(max_workers=workers))
    if debug:
        loop.set_debug(True)
    return loop


def run_multiple_browsers(workers_browsers=4, cims_per_task=20):
    loop = _loop(4, True)
    cims_list = CimsList.get_all()
    queue = create_queue(cims_list, cims_per_task)
    BASE_URL = "https://es.wikiloc.com/"

    loop.run_until_complete(run_multiple(BASE_URL, queue))


if __name__ == "__main__":
    """Run standallone wikiloc browser collector.

    Mainly for testing
    """
    driver = setup_browser()
    cims_lst = CimsList.get_all()[:3]
    url = "https://es.wikiloc.com/"
    wikiloc = WikiLoc(url)
    wikiloc.collect(driver, cims_lst)
