"""Application schemas."""
from typing import List

from pydantic import BaseModel


class Route(BaseModel):
    """Route obj schema."""

    id: int
    name: str
    uuid: str
    cim_uuid: str
    length: float
    type: str
    circular: bool
    ramp_up: float
    ramp_down: float
    max_hight: float
    min_hight: float
    difficulty: str
    url: str


class Cim(BaseModel):
    """Cim obj schema."""

    id: int
    uuid: str
    name: str
    region: str
    lat: float
    lng: float
    alt: int
    essential: bool
    url: str
    img_url: str
    routes: List[Route]
