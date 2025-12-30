"""Domain models."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class TimeSeriesReference:
    space: Optional[str] = None
    external_id: Optional[str] = None


@dataclass
class FacilityReference:
    space: Optional[str] = None
    external_id: Optional[str] = None


@dataclass
class FileReference:
    space: Optional[str] = None
    external_id: Optional[str] = None


@dataclass
class Facility:
    external_id: str
    space: str
    name: str
    desc: Optional[str] = None


@dataclass
class Pump:
    external_id: str
    space: str
    name: str
    year: Optional[int] = None
    weight: Optional[float] = None
    weight_unit: Optional[str] = None
    pressure: Optional[TimeSeriesReference] = None
    temperature: Optional[TimeSeriesReference] = None
    lives_in: Optional[FacilityReference] = None


@dataclass
class Documentation:
    external_id: str
    space: str
    name: Optional[str] = None
    file: Optional[FileReference] = None
