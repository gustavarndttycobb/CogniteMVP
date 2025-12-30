"""Router for Pump endpoints."""

from fastapi import APIRouter, HTTPException
from typing import Any
from cognite.client.data_classes.data_modeling import ViewId, NodeApply, NodeOrEdgeData

from ..cognite_client import get_cognite_client, get_data_model_info, get_view_id
from ..schemas import PumpResponse, ListResponse, PumpCreate

router = APIRouter(prefix="/pumps", tags=["Pumps"])


def _extract_reference(data: dict | None, ref_type: str) -> dict | None:
    """Extract reference data from Cognite response."""
    if data is None:
        return None
    if isinstance(data, dict):
        return {
            "space": data.get("space"),
            "external_id": data.get("externalId"),
        }
    return None


def _parse_pump(item: Any, view_id: ViewId) -> dict:
    """Parse pump instance from Cognite response."""
    properties = item.properties or {}
    
    # Get properties from the data model view
    view_props = properties.get(view_id, {})
    
    return {
        "external_id": item.external_id,
        "space": item.space,
        "name": view_props.get("name", ""),
        "year": view_props.get("year"),
        "weight": view_props.get("weight"),
        "weight_unit": view_props.get("weightUnit"),
        "pressure": _extract_reference(view_props.get("pressure"), "timeseries"),
        "temperature": _extract_reference(view_props.get("temperature"), "timeseries"),
        "lives_in": _extract_reference(view_props.get("livesIn"), "facility"),
    }


@router.get("", response_model=ListResponse)
async def list_pumps(limit: int = 100) -> ListResponse:
    """
    List all pumps from the data model.
    
    Args:
        limit: Maximum number of pumps to return (default: 100)
    
    Returns:
        List of pumps with their properties
    """
    try:
        client = get_cognite_client()
        view_id = get_view_id("Pump")
        
        # Query instances from the Pump view
        instances = client.data_modeling.instances.list(
            instance_type="node",
            sources=[(view_id.space, view_id.external_id, view_id.version)],
            limit=limit,
        )
        
        pumps = [_parse_pump(item, view_id) for item in instances]
        
        return ListResponse(items=pumps, count=len(pumps))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pumps: {str(e)}")


@router.get("/{external_id}", response_model=PumpResponse)
async def get_pump(external_id: str) -> PumpResponse:
    """
    Get a specific pump by external ID.
    
    Args:
        external_id: The external ID of the pump
    
    Returns:
        Pump details
    """
    try:
        client = get_cognite_client()
        view_id = get_view_id("Pump")
        space, _, _ = get_data_model_info()
        
        # Retrieve specific instance
        instances = client.data_modeling.instances.retrieve(
            nodes=[{"space": space, "externalId": external_id}],
            sources=[view_id],
        )
        
        if not instances.nodes:
            raise HTTPException(status_code=404, detail=f"Pump '{external_id}' not found")
        
        pump = _parse_pump(instances.nodes[0], view_id)
        return PumpResponse(**pump)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching pump: {str(e)}")

@router.post("", response_model=PumpResponse)
async def upsert_pump(pump: PumpCreate) -> PumpResponse:
    """
    Create or update a pump.
    
    Args:
        pump: The pump data to create or update
    
    Returns:
        The created/updated pump
    """
    try:
        client = get_cognite_client()
        view_id = get_view_id("Pump")
        
        properties = {
            "name": pump.name,
            "year": pump.year,
            "weight": pump.weight,
            "weightUnit": pump.weight_unit,
        }
        
        # Add references if present
        # Note: Cognite expects references as dicts with space and externalId
        if pump.pressure:
            properties["pressure"] = {"space": pump.pressure.space, "externalId": pump.pressure.external_id}
        if pump.temperature:
            properties["temperature"] = {"space": pump.temperature.space, "externalId": pump.temperature.external_id}
        if pump.lives_in:
            properties["livesIn"] = {"space": pump.lives_in.space, "externalId": pump.lives_in.external_id}
            
        # Create NodeApply object
        node = NodeApply(
            space=pump.space,
            external_id=pump.external_id,
            sources=[
                NodeOrEdgeData(
                    source=view_id,
                    properties=properties
                )
            ]
        )
        
        # Apply instance to Cognite
        res = client.data_modeling.instances.apply(nodes=[node])
        
        if not res.nodes:
             raise HTTPException(status_code=500, detail="Failed to create/update pump")
             
        return PumpResponse(
            external_id=pump.external_id,
            space=pump.space,
            name=pump.name,
            year=pump.year,
            weight=pump.weight,
            weight_unit=pump.weight_unit,
            pressure=pump.pressure,
            temperature=pump.temperature,
            lives_in=pump.lives_in
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating pump: {str(e)}")
