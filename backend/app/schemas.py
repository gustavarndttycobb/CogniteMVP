"""Pydantic schemas for API responses."""

from pydantic import BaseModel
from typing import Optional, Any


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"


class TimeSeriesReference(BaseModel):
    """Reference to a TimeSeries."""
    space: Optional[str] = None
    external_id: Optional[str] = None


class FacilityReference(BaseModel):
    """Reference to a Facility."""
    space: Optional[str] = None
    external_id: Optional[str] = None


class FileReference(BaseModel):
    """Reference to a File."""
    space: Optional[str] = None
    external_id: Optional[str] = None


class PumpResponse(BaseModel):
    """Pump data model response."""
    external_id: str
    space: str
    name: str
    year: Optional[int] = None
    weight: Optional[float] = None
    weight_unit: Optional[str] = None
    pressure: Optional[TimeSeriesReference] = None
    temperature: Optional[TimeSeriesReference] = None
    lives_in: Optional[FacilityReference] = None
    
    class Config:
        from_attributes = True


class FacilityResponse(BaseModel):
    """Facility data model response."""
    external_id: str
    space: str
    name: str
    desc: str
    
    class Config:
        from_attributes = True


class DocumentationResponse(BaseModel):
    """Documentation data model response."""
    external_id: str
    space: str
    name: Optional[str] = None
    file: Optional[FileReference] = None
    
    class Config:
        from_attributes = True


class FacilityCreate(BaseModel):
    """Schema for creating/updating a Facility."""
    external_id: str
    space: str
    name: str
    desc: Optional[str] = None


class PumpCreate(BaseModel):
    """Schema for creating/updating a Pump."""
    external_id: str
    space: str
    name: str
    year: Optional[int] = None
    weight: Optional[float] = None
    weight_unit: Optional[str] = None
    pressure: Optional[TimeSeriesReference] = None
    temperature: Optional[TimeSeriesReference] = None
    lives_in: Optional[FacilityReference] = None


class DocumentationCreate(BaseModel):
    """Schema for creating/updating a Documentation."""
    external_id: str
    space: str
    name: Optional[str] = None
    file: Optional[FileReference] = None


class ListResponse(BaseModel):
    """Generic list response wrapper."""
    items: list[Any]
    count: int
