"""Router for Documentation endpoints."""

from fastapi import APIRouter, HTTPException
from typing import Any
from cognite.client.data_classes.data_modeling import ViewId

from ..cognite_client import get_cognite_client, get_data_model_info, get_view_id
from ..schemas import DocumentationResponse, ListResponse

router = APIRouter(prefix="/documentations", tags=["Documentations"])


def _extract_file_reference(data: dict | None) -> dict | None:
    """Extract file reference data from Cognite response."""
    if data is None:
        return None
    if isinstance(data, dict):
        return {
            "space": data.get("space"),
            "external_id": data.get("externalId"),
        }
    return None


def _parse_documentation(item: Any, view_id: ViewId) -> dict:
    """Parse documentation instance from Cognite response."""
    properties = item.properties or {}
    
    # Get properties from the data model view
    view_props = properties.get(view_id, {})
    
    return {
        "external_id": item.external_id,
        "space": item.space,
        "name": view_props.get("name"),
        "file": _extract_file_reference(view_props.get("file")),
    }


@router.get("", response_model=ListResponse)
async def list_documentations(limit: int = 100) -> ListResponse:
    """
    List all documentations from the data model.
    
    Args:
        limit: Maximum number of documentations to return (default: 100)
    
    Returns:
        List of documentations with their properties
    """
    try:
        client = get_cognite_client()
        view_id = get_view_id("Documentation")
        
        # Query instances from the Documentation view
        instances = client.data_modeling.instances.list(
            instance_type="node",
            sources=[(view_id.space, view_id.external_id, view_id.version)],
            limit=limit,
        )
        
        docs = [_parse_documentation(item, view_id) for item in instances]
        
        return ListResponse(items=docs, count=len(docs))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching documentations: {str(e)}")


@router.get("/{external_id}", response_model=DocumentationResponse)
async def get_documentation(external_id: str) -> DocumentationResponse:
    """
    Get a specific documentation by external ID.
    
    Args:
        external_id: The external ID of the documentation
    
    Returns:
        Documentation details
    """
    try:
        client = get_cognite_client()
        view_id = get_view_id("Documentation")
        space, _, _ = get_data_model_info()
        
        # Retrieve specific instance
        instances = client.data_modeling.instances.retrieve(
            nodes=[{"space": space, "externalId": external_id}],
            sources=[view_id],
        )
        
        if not instances.nodes:
            raise HTTPException(status_code=404, detail=f"Documentation '{external_id}' not found")
        
        doc = _parse_documentation(instances.nodes[0], view_id)
        return DocumentationResponse(**doc)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching documentation: {str(e)}")
