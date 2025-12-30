from typing import Any
from ...infrastructure.cognite.client import get_cognite_client

class FileRepository:
    def __init__(self):
        self.client = get_cognite_client()

    def upload_bytes(self, content: bytes, name: str, external_id: str, mime_type: str, overwrite: bool = True) -> Any:
        return self.client.files.upload_bytes(
            content=content,
            name=name,
            external_id=external_id,
            mime_type=mime_type,
            overwrite=overwrite
        )
