from typing import List, Optional, Any
from cognite.client.data_classes.data_modeling import ViewId, NodeApply, NodeOrEdgeData

from ...domain.models import Facility
from ...domain.interfaces import FacilityRepository
from ...infrastructure.cognite.client import get_cognite_client, get_view_id, get_data_model_info

class CogniteFacilityRepository(FacilityRepository):
    def __init__(self):
        self.client = get_cognite_client()
        self.view_id = get_view_id("Facility")
        self.space, _, _ = get_data_model_info()

    def _parse_facility(self, item: Any) -> Facility:
        properties = item.properties or {}
        view_props = properties.get(self.view_id, {})
        
        return Facility(
            external_id=item.external_id,
            space=item.space,
            name=view_props.get("name", ""),
            desc=view_props.get("desc", ""),
        )

    def list(self, limit: int = 100) -> List[Facility]:
        instances = self.client.data_modeling.instances.list(
            instance_type="node",
            sources=[(self.view_id.space, self.view_id.external_id, self.view_id.version)],
            limit=limit,
        )
        return [self._parse_facility(item) for item in instances]

    def get(self, external_id: str) -> Optional[Facility]:
        instances = self.client.data_modeling.instances.retrieve(
            nodes=[{"space": self.space, "externalId": external_id}],
            sources=[self.view_id],
        )
        if not instances.nodes:
            return None
        return self._parse_facility(instances.nodes[0])

    def upsert(self, facility: Facility) -> Facility:
        node = NodeApply(
            space=facility.space,
            external_id=facility.external_id,
            sources=[
                NodeOrEdgeData(
                    source=self.view_id,
                    properties={
                        "name": facility.name,
                        "desc": facility.desc,
                    }
                )
            ]
        )
        res = self.client.data_modeling.instances.apply(nodes=[node])
        if not res.nodes:
            raise Exception("Failed to create/update facility")
        
        return facility
