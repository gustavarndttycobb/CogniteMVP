"""Router for debugging Cognite data model."""

from fastapi import APIRouter, HTTPException

from ...infrastructure.cognite.client import get_cognite_client, get_data_model_info

router = APIRouter(prefix="/debug", tags=["Debug"])


@router.get("/views")
async def list_views():
    """
    List all views in the configured space.
    This helps debug which views are available.
    """
    try:
        client = get_cognite_client()
        space, model_name, version = get_data_model_info()
        
        # List all views in the space
        views = client.data_modeling.views.list(space=space, limit=100)
        
        result = []
        for view in views:
            result.append({
                "space": view.space,
                "external_id": view.external_id,
                "version": view.version,
                "name": view.name,
                "description": view.description,
            })
        
        return {
            "configured_space": space,
            "configured_model": model_name,
            "configured_version": version,
            "views": result,
            "count": len(result),
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing views: {str(e)}")


@router.get("/data-models")
async def list_data_models():
    """
    List all data models in the configured space.
    """
    try:
        client = get_cognite_client()
        space, model_name, version = get_data_model_info()
        
        # List all data models
        models = client.data_modeling.data_models.list(space=space, limit=100)
        
        result = []
        for model in models:
            result.append({
                "space": model.space,
                "external_id": model.external_id,
                "version": model.version,
                "name": model.name,
                "description": model.description,
                "views": [
                    {
                        "space": v.space,
                        "external_id": v.external_id,
                        "version": v.version,
                    }
                    for v in (model.views or [])
                ],
            })
        
        return {
            "configured_space": space,
            "configured_model": model_name,
            "configured_version": version,
            "data_models": result,
            "count": len(result),
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing data models: {str(e)}")
