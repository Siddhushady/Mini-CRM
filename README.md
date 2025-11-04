# Mini CRM (Simple demo)

## Run locally (no Docker)
1. Create virtualenv & install:

python -m venv .venv
source .venv/bin/activate # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

2. Initialize DB:

python init_db.py

3. Run:

python app.py

4. Open http://localhost:5000

## Run with Docker
1. Build & run:

docker compose up --build

2. Visit http://localhost:5000

## Useful endpoints
- UI: / (dashboard), /leads, /lead/add
- API: GET/POST /api/leads
- Automation (simulate): POST /automation/run
- Preview automation changes (no commit): GET /api/automation/preview
