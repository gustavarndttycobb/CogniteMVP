from typing import List, Optional
from ..domain.models import Documentation, FileReference
from ..domain.interfaces import DocumentationRepository
from ..infrastructure.repositories.file_repository import FileRepository

class DocumentationService:
    def __init__(self, doc_repository: DocumentationRepository, file_repository: FileRepository):
        self.doc_repository = doc_repository
        self.file_repository = file_repository

    def list_documentations(self, limit: int = 100) -> List[Documentation]:
        return self.doc_repository.list(limit)

    def get_documentation(self, external_id: str) -> Optional[Documentation]:
        return self.doc_repository.get(external_id)

    def upsert_documentation(self, documentation: Documentation) -> Documentation:
        return self.doc_repository.upsert(documentation)

    def upload_and_create(self, content: bytes, filename: str, mime_type: str, 
                         doc_external_id: str, space: str, name: str) -> Documentation:
        # 1. Upload file
        file_external_id = f"{doc_external_id}_file"
        self.file_repository.upload_bytes(
            content=content,
            name=filename,
            external_id=file_external_id,
            mime_type=mime_type
        )
        
        # 2. Create Documentation
        doc = Documentation(
            external_id=doc_external_id,
            space=space,
            name=name,
            file=FileReference(external_id=file_external_id)
        )
        
        return self.doc_repository.upsert(doc)
