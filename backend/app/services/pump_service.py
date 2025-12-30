from typing import List, Optional
from ..domain.models import Pump
from ..domain.interfaces import PumpRepository

class PumpService:
    def __init__(self, repository: PumpRepository):
        self.repository = repository

    def list_pumps(self, limit: int = 100) -> List[Pump]:
        return self.repository.list(limit)

    def get_pump(self, external_id: str) -> Optional[Pump]:
        return self.repository.get(external_id)

    def upsert_pump(self, pump: Pump) -> Pump:
        return self.repository.upsert(pump)
