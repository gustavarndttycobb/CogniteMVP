from functools import lru_cache
from ..infrastructure.repositories.facility_repository import CogniteFacilityRepository
from ..infrastructure.repositories.pump_repository import CognitePumpRepository
from ..infrastructure.repositories.documentation_repository import CogniteDocumentationRepository
from ..infrastructure.repositories.file_repository import FileRepository
from ..services.facility_service import FacilityService
from ..services.pump_service import PumpService
from ..services.documentation_service import DocumentationService

@lru_cache
def get_facility_service() -> FacilityService:
    repository = CogniteFacilityRepository()
    return FacilityService(repository)

@lru_cache
def get_pump_service() -> PumpService:
    repository = CognitePumpRepository()
    return PumpService(repository)

@lru_cache
def get_documentation_service() -> DocumentationService:
    doc_repo = CogniteDocumentationRepository()
    file_repo = FileRepository()
    return DocumentationService(doc_repo, file_repo)

@lru_cache
def get_file_repository() -> FileRepository:
    return FileRepository()
