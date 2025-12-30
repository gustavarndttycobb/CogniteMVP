from fastapi import APIRouter, HTTPException, Depends
from ..schemas import FacilityResponse, ListResponse, FacilityCreate
from ..dependencies import get_facility_service
from ...services.facility_service import FacilityService
from ...domain.models import Facility

router = APIRouter(prefix="/facilities", tags=["Facilities"])

@router.get("", response_model=ListResponse)
async def list_facilities(
    limit: int = 100,
    service: FacilityService = Depends(get_facility_service)
) -> ListResponse:
    try:
        facilities = service.list_facilities(limit)
        # Convert domain models to response models implicitly or explicitly
        # Pydantic's from_attributes=True handles dataclasses
        return ListResponse(items=facilities, count=len(facilities))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching facilities: {str(e)}")

@router.get("/{external_id}", response_model=FacilityResponse)
async def get_facility(
    external_id: str,
    service: FacilityService = Depends(get_facility_service)
) -> FacilityResponse:
    try:
        facility = service.get_facility(external_id)
        if not facility:
            raise HTTPException(status_code=404, detail=f"Facility '{external_id}' not found")
        return FacilityResponse.model_validate(facility)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching facility: {str(e)}")

@router.post("", response_model=FacilityResponse)
async def upsert_facility(
    facility: FacilityCreate,
    service: FacilityService = Depends(get_facility_service)
) -> FacilityResponse:
    try:
        domain_facility = Facility(
            external_id=facility.external_id,
            space=facility.space,
            name=facility.name,
            desc=facility.desc
        )
        created = service.upsert_facility(domain_facility)
        return FacilityResponse.model_validate(created)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating facility: {str(e)}")
