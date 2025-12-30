from fastapi import APIRouter, HTTPException, Depends
from ..schemas import PumpResponse, ListResponse, PumpCreate
from ..dependencies import get_pump_service
from ...services.pump_service import PumpService
from ...domain.models import Pump, TimeSeriesReference, FacilityReference

router = APIRouter(prefix="/pumps", tags=["Pumps"])

@router.get("", response_model=ListResponse)
async def list_pumps(
    limit: int = 100,
    service: PumpService = Depends(get_pump_service)
) -> ListResponse:
    try:
        pumps = service.list_pumps(limit)
        return ListResponse(items=pumps, count=len(pumps))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pumps: {str(e)}")

@router.get("/{external_id}", response_model=PumpResponse)
async def get_pump(
    external_id: str,
    service: PumpService = Depends(get_pump_service)
) -> PumpResponse:
    try:
        pump = service.get_pump(external_id)
        if not pump:
            raise HTTPException(status_code=404, detail=f"Pump '{external_id}' not found")
        return PumpResponse.model_validate(pump)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pump: {str(e)}")

@router.post("", response_model=PumpResponse)
async def upsert_pump(
    pump: PumpCreate,
    service: PumpService = Depends(get_pump_service)
) -> PumpResponse:
    try:
        # Convert Pydantic models to Domain models
        pressure = TimeSeriesReference(**pump.pressure.model_dump()) if pump.pressure else None
        temperature = TimeSeriesReference(**pump.temperature.model_dump()) if pump.temperature else None
        lives_in = FacilityReference(**pump.lives_in.model_dump()) if pump.lives_in else None

        domain_pump = Pump(
            external_id=pump.external_id,
            space=pump.space,
            name=pump.name,
            year=pump.year,
            weight=pump.weight,
            weight_unit=pump.weight_unit,
            pressure=pressure,
            temperature=temperature,
            lives_in=lives_in
        )
        created = service.upsert_pump(domain_pump)
        return PumpResponse.model_validate(created)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating pump: {str(e)}")
