"""Domain repository interfaces."""

from abc import ABC, abstractmethod
from typing import List, Optional
from .models import Facility, Pump, Documentation


class FacilityRepository(ABC):
    @abstractmethod
    def list(self, limit: int = 100) -> List[Facility]:
        pass

    @abstractmethod
    def get(self, external_id: str) -> Optional[Facility]:
        pass

    @abstractmethod
    def upsert(self, facility: Facility) -> Facility:
        pass


class PumpRepository(ABC):
    @abstractmethod
    def list(self, limit: int = 100) -> List[Pump]:
        pass

    @abstractmethod
    def get(self, external_id: str) -> Optional[Pump]:
        pass

    @abstractmethod
    def upsert(self, pump: Pump) -> Pump:
        pass


class DocumentationRepository(ABC):
    @abstractmethod
    def list(self, limit: int = 100) -> List[Documentation]:
        pass

    @abstractmethod
    def get(self, external_id: str) -> Optional[Documentation]:
        pass

    @abstractmethod
    def upsert(self, documentation: Documentation) -> Documentation:
        pass
