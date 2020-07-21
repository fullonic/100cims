"""Ram database for dev."""

from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

import ujson

from server.data_collector.feec import CimsList
from server.schemas import Cim


@lru_cache
def get_cims() -> dict:
    return CimsList.as_dict()


CIMS = get_cims()


@dataclass
class DataBase:
    """In memory database."""

    routes: list = field(default_factory=list)
    search_urls: list = field(default_factory=list)
    updated_cims: dict = field(default_factory=dict)
    data: list = field(default_factory=list)

    def add(self, data):
        """Commit data into memory session."""
        print("Adding to in memory database")

        if data.get("routes", False):
            print("Here")
            # search cim by UUID
            for el in data["routes"]:
                uuid = list(el.keys())[0]
                print(f"Saving {uuid}")
                # search for cims uuid on list
                try:
                    cim = CIMS.get(uuid, None)
                    routes = el[uuid]["trekking"]
                    # add routes to route el
                    cim["routes"] = routes
                    self.updated_cims[uuid] = cim
                    self.routes.append(routes)
                except KeyError:
                    print(f"UUID not found: {uuid}")
        return self.updated_cims

    def commit(self):
        """Commit data into file."""
        with open("routes_cims.json", "w") as f:
            ujson.dump(self.updated_cims, f)
        print(f"Commit {len(self.updated_cims)} cims into ujson file")

    def get_all(self, schema: bool = True):
        """Get all cims from in memory database."""

        cims_db = Path(__file__).parent / "data_collector/cims_db.json"
        if len(self.data) == 0:  # avoids call again if already loaded
            with open(cims_db) as f:
                data = ujson.load(f)
            if schema:
                for cim in data:
                    self.data.append(Cim(**data[cim]))
            else:
                self.data = data
        return self.data

    def get(self, id_):
        """Get a single cim by id."""
        data = self.get_all(True)
        return data[id_ - 1]


RAMDB = DataBase()
