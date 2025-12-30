"""Cognite SDK client configuration with Token-based authentication."""

from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import Token
from cognite.client.data_classes.data_modeling import ViewId
from functools import lru_cache
import os

from ...core.config import get_settings


def get_cognite_client() -> CogniteClient:
    """
    Get a Cognite client instance with Token-based authentication.
    
    The token should be set in the COGNITE_TOKEN environment variable.
    You can get this token from the Cognite Fusion web interface after logging in.
    """
    settings = get_settings()
    
    # Get token from environment variable
    token = os.getenv("COGNITE_TOKEN")
    if not token:
        raise ValueError(
            "COGNITE_TOKEN environment variable is not set. "
            "Please set it with your access token from Cognite Fusion."
        )
    
    # Token-based credentials
    credentials = Token(token)
    
    config = ClientConfig(
        client_name="cognite-mvp-api",
        project=settings.cognite_project,
        base_url=settings.cognite_base_url,
        credentials=credentials,
    )
    
    return CogniteClient(config)


def get_data_model_info() -> tuple[str, str, str]:
    """Get data model space, name, and version from settings."""
    settings = get_settings()
    return (
        settings.data_model_space,
        settings.data_model_name,
        settings.data_model_version,
    )


def get_view_id(view_name: str) -> ViewId:
    """
    Get a ViewId for the specified view name by looking up the actual version.
    
    The version is discovered dynamically from the Cognite API.
    """
    client = get_cognite_client()
    space, _, _ = get_data_model_info()
    
    # List views and find the one we need
    views = client.data_modeling.views.list(space=space, limit=100)
    
    for view in views:
        if view.external_id == view_name:
            return ViewId(space=view.space, external_id=view.external_id, version=view.version)
    
    raise ValueError(f"View '{view_name}' not found in space '{space}'")
