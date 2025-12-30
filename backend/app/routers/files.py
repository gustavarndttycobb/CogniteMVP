from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
from ..cognite_client import get_cognite_client

router = APIRouter(prefix="/files", tags=["Files"])

@router.post("/upload")
async def upload_file(
    file: UploadFile = File(...), 
    external_id: Optional[str] = Form(None)
) -> dict:
    """
    Upload a file to Cognite Data Fusion.
    
    Args:
        file: The file to upload
        external_id: Optional external ID for the file. If not provided, filename is used.
    
    Returns:
        Metadata of the uploaded file
    """
    try:
        client = get_cognite_client()
        
        # Read file content
        content = await file.read()
        
        # Use filename as external_id if not provided
        if not external_id:
            external_id = file.filename
            
        # Upload to CDF
        # Using overwrite=True to simplify development/testing
        res = client.files.upload_bytes(
            content=content,
            name=file.filename,
            external_id=external_id,
            mime_type=file.content_type,
            overwrite=True
        )
        
        return {
            "id": res.id,
            "external_id": res.external_id,
            "name": res.name,
            "uploaded": res.uploaded,
            "mime_type": res.mime_type
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")
