"""Inspect Documentation view properties."""
import sys
import os

# Add current directory to path so we can import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import get_settings
from app.infrastructure.cognite.client import get_cognite_client, get_view_id

# Get settings
settings = get_settings()

# Create client
try:
    client = get_cognite_client()
except Exception as e:
    print(f"Error initializing client: {e}")
    exit(1)

# Get Documentation view
space = settings.data_model_space
external_id = "Documentation"

print(f"Retrieving view {space}:{external_id} (latest version)...")
try:
    # Use the helper to get the correct version dynamically
    view_id = get_view_id(external_id)
    print(f"Resolved ViewId: {view_id}")

    views = client.data_modeling.views.retrieve(ids=[view_id])
    
    if views:
        view = views[0]
        print(f"View found: {view.external_id}")
        if "file" in view.properties:
            prop = view.properties["file"]
            print(f"Property 'file': {prop}")
            print(f"Type: {type(prop)}")
            # Print details
            if hasattr(prop, "type"):
                print(f"Prop Type: {prop.type}")
        else:
            print("Property 'file' not found in view!")
            print("Available properties:", view.properties.keys())
    else:
        print("View not found!")

except Exception as e:
    print(f"Error: {e}")
