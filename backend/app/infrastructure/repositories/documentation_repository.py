from typing import List, Optional, Any
from cognite.client.data_classes.data_modeling import ViewId, NodeApply, NodeOrEdgeData

from ...domain.models import Documentation, FileReference
from ...domain.interfaces import DocumentationRepository
from ...infrastructure.cognite.client import get_cognite_client, get_view_id, get_data_model_info

class CogniteDocumentationRepository(DocumentationRepository):
    def __init__(self):
        self.client = get_cognite_client()
        self.view_id = get_view_id("Documentation")
        self.space, _, _ = get_data_model_info()

    def _extract_file_reference(self, data: Any) -> Optional[FileReference]:
        if data is None:
            return None
        
        if isinstance(data, str):
             return FileReference(external_id=data)
        
        if isinstance(data, dict):
            return FileReference(
                space=data.get("space"),
                external_id=data.get("externalId")
            )
        return None

    def _parse_documentation(self, item: Any) -> Documentation:
        properties = item.properties or {}
        view_props = properties.get(self.view_id, {})
        
        return Documentation(
            external_id=item.external_id,
            space=item.space,
            name=view_props.get("name"),
            file=self._extract_file_reference(view_props.get("file")),
        )

    def list(self, limit: int = 100) -> List[Documentation]:
        instances = self.client.data_modeling.instances.list(
            instance_type="node",
            sources=[(self.view_id.space, self.view_id.external_id, self.view_id.version)],
            limit=limit,
        )
        return [self._parse_documentation(item) for item in instances]

    def get(self, external_id: str) -> Optional[Documentation]:
        instances = self.client.data_modeling.instances.retrieve(
            nodes=[{"space": self.space, "externalId": external_id}],
            sources=[self.view_id],
        )
        if not instances.nodes:
            return None
        return self._parse_documentation(instances.nodes[0])

    def upsert(self, documentation: Documentation) -> Documentation:
        properties = {
            "name": documentation.name,
        }
        
        if documentation.file:
            # We know it expects a string externalId
            properties["file"] = documentation.file.external_id

        node = NodeApply(
            space=documentation.space,
            external_id=documentation.external_id,
            sources=[
                NodeOrEdgeData(
                    source=self.view_id,
                    properties=properties
                )
            ]
        )
        res = self.client.data_modeling.instances.apply(nodes=[node])
        if not res.nodes:
            raise Exception("Failed to create/update documentation")
        
        return documentation
