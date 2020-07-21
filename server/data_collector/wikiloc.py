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
