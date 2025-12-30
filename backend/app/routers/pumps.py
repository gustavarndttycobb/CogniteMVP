"""Router for Pump endpoints."""

from fastapi import APIRouter, HTTPException
from typing import Any
from cognite.client.data_classes.data_modeling import ViewId

from ..cognite_client import get_cognite_client, get_data_model_info, get_view_id
from ..schemas import PumpResponse, ListResponse

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
