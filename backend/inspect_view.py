"""Inspect Documentation view properties."""
import os
from cognite.client import CogniteClient, ClientConfig
from cognite.client.credentials import Token
from cognite.client.data_classes.data_modeling import ViewId

# Set token
token = os.getenv("COGNITE_TOKEN")
if not token:
    print("Please set COGNITE_TOKEN environment variable")
    exit(1)

# Create client
credentials = Token(token)
config = ClientConfig(
    client_name="test-script",
    project="radix-dev",
    base_url="https://az-eastus-1.cognitedata.com",
    credentials=credentials,
)
client = CogniteClient(config)

# Get Documentation view
# Note: version hash from previous steps
version = "adbba6e034213a" 
space = "ARNDT_SPACE_TEST"
external_id = "Documentation"

print(f"Retrieving view {space}:{external_id}/{version}...")
try:
    views = client.data_modeling.views.retrieve(
        ids=[ViewId(space=space, external_id=external_id, version=version)]
    )
    
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
