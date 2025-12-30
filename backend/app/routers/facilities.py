"""Router for Facility endpoints."""

from fastapi import APIRouter, HTTPException
from typing import Any
from cognite.client.data_classes.data_modeling import ViewId, NodeApply, NodeOrEdgeData

from ..cognite_client import get_cognite_client, get_data_model_info, get_view_id
from ..schemas import FacilityResponse, ListResponse, FacilityCreate

router = APIRouter(prefix="/facilities", tags=["Facilities"])


def _parse_facility(item: Any, view_id: ViewId) -> dict:
    """Parse facility instance from Cognite response."""
    properties = item.properties or {}
    
    # Get properties from the data model view
    # The SDK's properties object expects a ViewId key, not space string
    view_props = properties.get(view_id, {})
    
    return {
        "external_id": item.external_id,
        "space": item.space,
        "name": view_props.get("name", ""),
        "desc": view_props.get("desc", ""),
    }




@router.get("", response_model=ListResponse)
async def list_facilities(limit: int = 100) -> ListResponse:
    """
    List all facilities from the data model.
    
    Args:
        limit: Maximum number of facilities to return (default: 100)
    
    Returns:
        List of facilities with their properties
    """
    try:
        client = get_cognite_client()
        view_id = get_view_id("Facility")
        
        # Query instances from the Facility view
        # Using tuple format to avoid potential ViewId object issues
        instances = client.data_modeling.instances.list(
            instance_type="node",
            sources=[(view_id.space, view_id.external_id, view_id.version)],
            limit=limit,
        )
        
        facilities = [_parse_facility(item, view_id) for item in instances]
        
        return ListResponse(items=facilities, count=len(facilities))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching facilities: {str(e)}")


@router.get("/{external_id}", response_model=FacilityResponse)
async def get_facility(external_id: str) -> FacilityResponse:
    """
    Get a specific facility by external ID.
    
    Args:
        external_id: The external ID of the facility
    
    Returns:
        Facility details
    """
    try:
        client = get_cognite_client()
        view_id = get_view_id("Facility")
        space, _, _ = get_data_model_info()
        
        # Retrieve specific instance
        instances = client.data_modeling.instances.retrieve(
            nodes=[{"space": space, "externalId": external_id}],
            sources=[view_id],
        )
        
        if not instances.nodes:
            raise HTTPException(status_code=404, detail=f"Facility '{external_id}' not found")
        
        facility = _parse_facility(instances.nodes[0], view_id)
        return FacilityResponse(**facility)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching facility: {str(e)}")


@router.post("", response_model=FacilityResponse)
async def upsert_facility(facility: FacilityCreate) -> FacilityResponse:
    """
    Create or update a facility.
    
    Args:
        facility: The facility data to create or update
    
    Returns:
        The created/updated facility
    """
    try:
        client = get_cognite_client()
        view_id = get_view_id("Facility")
        
        # Create NodeApply object
        node = NodeApply(
            space=facility.space,
            external_id=facility.external_id,
            sources=[
                NodeOrEdgeData(
                    source=view_id,
                    properties={
                        "name": facility.name,
                        "desc": facility.desc,
                    }
                )
            ]
        )
        
        # Apply instance to Cognite
        res = client.data_modeling.instances.apply(nodes=[node])
        
        if not res.nodes:
             raise HTTPException(status_code=500, detail="Failed to create/update facility")
        
        # Return response based on input data
        return FacilityResponse(
            external_id=facility.external_id,
            space=facility.space,
            name=facility.name,
            desc=facility.desc or ""
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating facility: {str(e)}")
