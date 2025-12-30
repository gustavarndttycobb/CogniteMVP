"""Test script to debug Cognite API access."""
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

# Get views
space = "ARNDT_SPACE_TEST"
print(f"Listing views in space: {space}")
views = client.data_modeling.views.list(space=space, limit=100)
print(f"Found {len(views)} views:")
for view in views:
    print(f"  - {view.external_id} (version: {view.version})")

# Get Facility view
facility_view = None
for view in views:
    if view.external_id == "Facility":
        facility_view = view
        break

if facility_view:
    print(f"\nFacility view found:")
    print(f"  Space: {facility_view.space}")
    print(f"  External ID: {facility_view.external_id}")
    print(f"  Version: {facility_view.version}")
    
    # Create ViewId
    view_id = ViewId(space=facility_view.space, external_id=facility_view.external_id, version=facility_view.version)
    print(f"\nViewId created: {view_id}")
    print(f"ViewId type: {type(view_id)}")
    
    # Try to list instances
    print(f"\nListing instances using view_id...")
    try:
        instances = client.data_modeling.instances.list(
            instance_type="node",
            sources=[view_id],
            limit=5,
        )
        print(f"Found {len(instances)} instances")
        for inst in instances:
            print(f"  - {inst.external_id}")
    except Exception as e:
        print(f"Error: {e}")
        
        # Try with the view object directly
        print(f"\nTrying with view object directly...")
        try:
            instances = client.data_modeling.instances.list(
                instance_type="node",
                sources=[facility_view],
                limit=5,
            )
            print(f"Found {len(instances)} instances")
            for inst in instances:
                print(f"  - {inst.external_id}")
        except Exception as e2:
            print(f"Error with view object: {e2}")
else:
    print("Facility view not found!")
