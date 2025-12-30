from typing import List, Optional, Any
from cognite.client.data_classes.data_modeling import ViewId, NodeApply, NodeOrEdgeData

from ...domain.models import Pump, TimeSeriesReference, FacilityReference
from ...domain.interfaces import PumpRepository
from ...infrastructure.cognite.client import get_cognite_client, get_view_id, get_data_model_info

class CognitePumpRepository(PumpRepository):
    def __init__(self):
        self.client = get_cognite_client()
        self.view_id = get_view_id("Pump")
        self.space, _, _ = get_data_model_info()

    def _extract_reference(self, data: dict | None, ref_type: str) -> Any:
        if data is None:
            return None
        if isinstance(data, dict):
            space = data.get("space")
            external_id = data.get("externalId")
            if ref_type == "timeseries":
                return TimeSeriesReference(space=space, external_id=external_id)
            elif ref_type == "facility":
                return FacilityReference(space=space, external_id=external_id)
        return None

    def _parse_pump(self, item: Any) -> Pump:
        properties = item.properties or {}
        view_props = properties.get(self.view_id, {})
        
        return Pump(
            external_id=item.external_id,
            space=item.space,
            name=view_props.get("name", ""),
            year=view_props.get("year"),
            weight=view_props.get("weight"),
            weight_unit=view_props.get("weightUnit"),
            pressure=self._extract_reference(view_props.get("pressure"), "timeseries"),
            temperature=self._extract_reference(view_props.get("temperature"), "timeseries"),
            lives_in=self._extract_reference(view_props.get("livesIn"), "facility"),
        )

    def list(self, limit: int = 100) -> List[Pump]:
        instances = self.client.data_modeling.instances.list(
            instance_type="node",
            sources=[(self.view_id.space, self.view_id.external_id, self.view_id.version)],
            limit=limit,
        )
        return [self._parse_pump(item) for item in instances]

    def get(self, external_id: str) -> Optional[Pump]:
        instances = self.client.data_modeling.instances.retrieve(
            nodes=[{"space": self.space, "externalId": external_id}],
            sources=[self.view_id],
        )
        if not instances.nodes:
            return None
        return self._parse_pump(instances.nodes[0])

    def upsert(self, pump: Pump) -> Pump:
        properties = {
            "name": pump.name,
            "year": pump.year,
            "weight": pump.weight,
            "weightUnit": pump.weight_unit,
        }
        
        if pump.pressure:
            properties["pressure"] = {"space": pump.pressure.space, "externalId": pump.pressure.external_id}
        if pump.temperature:
            properties["temperature"] = {"space": pump.temperature.space, "externalId": pump.temperature.external_id}
        if pump.lives_in:
            properties["livesIn"] = {"space": pump.lives_in.space, "externalId": pump.lives_in.external_id}

        node = NodeApply(
            space=pump.space,
            external_id=pump.external_id,
            sources=[
                NodeOrEdgeData(
                    source=self.view_id,
                    properties=properties
                )
            ]
        )
        res = self.client.data_modeling.instances.apply(nodes=[node])
        if not res.nodes:
            raise Exception("Failed to create/update pump")
        
        return pump
