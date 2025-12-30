from typing import List, Optional
from ..domain.models import Facility
from ..domain.interfaces import FacilityRepository

class FacilityService:
    def __init__(self, repository: FacilityRepository):
        self.repository = repository

    def list_facilities(self, limit: int = 100) -> List[Facility]:
        return self.repository.list(limit)

    def get_facility(self, external_id: str) -> Optional[Facility]:
        return self.repository.get(external_id)

    def upsert_facility(self, facility: Facility) -> Facility:
        return self.repository.upsert(facility)
