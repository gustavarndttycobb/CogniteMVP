# Cognite MVP API

Minimal Python FastAPI application that integrates with Cognite Data Fusion to list data from the ARNDT_TEST data model.

## Setup

### 1. Create virtual environment

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Get your Cognite Token

1. Open [Cognite Fusion](https://radix.fusion.cognite.com)
2. Login with your Radix Microsoft account
3. Click your profile icon (top right)
4. Click "Copy token" or find the access token

### 4. Set the token and run

**Windows (PowerShell):**
```powershell
$env:COGNITE_TOKEN="your_token_here"
uvicorn app.main:app --reload
```

**Windows (CMD):**
```cmd
set COGNITE_TOKEN=your_token_here
uvicorn app.main:app --reload
```

**Linux/Mac:**
```bash
export COGNITE_TOKEN="your_token_here"
uvicorn app.main:app --reload
```

The API will start at http://localhost:8000

> **Note:** Tokens expire after some time. If you get authentication errors, get a new token from Cognite Fusion.

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check |
| GET | `/pumps` | List all pumps |
| GET | `/pumps/{external_id}` | Get pump by ID |
| GET | `/facilities` | List all facilities |
| GET | `/facilities/{external_id}` | Get facility by ID |
| GET | `/documentations` | List all documentations |
| GET | `/documentations/{external_id}` | Get documentation by ID |

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

Default configuration is set for:
- **Project**: radix-dev
- **Cluster**: az-eastus-1.cognitedata.com
- **Space**: ARNDT_SPACE_TEST
- **Data Model**: ARNDT_TEST
- **Version**: 1

To override, create a `.env` file (see `.env.example`).
