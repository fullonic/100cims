from typing import List

from selenium import webdriver

from server.schemas import Cim
from .data_collector.wikiloc import WikiLoc

from queue import Queue

_db = Queue()


def add_to_database(data):
    _db.put(data)
    return _db


def wikiloc_collect(driver: webdriver, url: str, cims_list: List[Cim]):
    """Top level call for wikiloc browser data collect."""
    wikiloc = WikiLoc(url)
    cims_info = wikiloc.collect(driver, cims_list)
    db_data = add_to_database(cims_info)
    print(db_data.qsize())
    # wikiloc.save(True, True)
    driver.close()
    print("Browser closed")
