from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Form
from ..schemas import DocumentationResponse, ListResponse, DocumentationCreate
from ..dependencies import get_documentation_service
from ...services.documentation_service import DocumentationService
from ...domain.models import Documentation, FileReference

router = APIRouter(prefix="/documentations", tags=["Documentations"])

@router.get("", response_model=ListResponse)
async def list_documentations(
    limit: int = 100,
    service: DocumentationService = Depends(get_documentation_service)
) -> ListResponse:
    try:
        docs = service.list_documentations(limit)
        return ListResponse(items=docs, count=len(docs))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching documentations: {str(e)}")

@router.get("/{external_id}", response_model=DocumentationResponse)
async def get_documentation(
    external_id: str,
    service: DocumentationService = Depends(get_documentation_service)
) -> DocumentationResponse:
    try:
        doc = service.get_documentation(external_id)
        if not doc:
            raise HTTPException(status_code=404, detail=f"Documentation '{external_id}' not found")
        return DocumentationResponse.model_validate(doc)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching documentation: {str(e)}")

@router.post("", response_model=DocumentationResponse)
async def upsert_documentation(
    doc: DocumentationCreate,
    service: DocumentationService = Depends(get_documentation_service)
) -> DocumentationResponse:
    try:
        file_ref = FileReference(**doc.file.model_dump()) if doc.file else None
        
        domain_doc = Documentation(
            external_id=doc.external_id,
            space=doc.space,
            name=doc.name,
            file=file_ref
        )
        created = service.upsert_documentation(domain_doc)
        return DocumentationResponse.model_validate(created)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating documentation: {str(e)}")

@router.post("/upload", response_model=DocumentationResponse)
async def upload_and_create_documentation(
    file: UploadFile = File(...),
    external_id: str = Form(...),
    space: str = Form(...),
    name: str = Form(...),
    service: DocumentationService = Depends(get_documentation_service)
) -> DocumentationResponse:
    try:
        content = await file.read()
        created = service.upload_and_create(
            content=content,
            filename=file.filename,
            mime_type=file.content_type,
            doc_external_id=external_id,
            space=space,
            name=name
        )
        return DocumentationResponse.model_validate(created)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
