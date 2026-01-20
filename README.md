\# Medical Telegram Warehouse - Complete Project

## 📊 Project Status & Interim Feedback Fixes

✅ **All interim feedback items addressed:**

| Feedback Item | Fix Implemented |
|---------------|-----------------|
| **Add all specified channels** | Added CheMed123, ethiopharma, pharmacyaddis, addispharma |
| **Improve logging** | Per-channel & date status logging with error handling |
| **PostgreSQL loader** | `src/load_to_postgres.py` with raw schema |
| **Complete star schema** | `dim_channels`, `dim_dates`, `fct_messages` models |
| **dbt tests** | `schema.yml` with unique, not_null, relationships tests |
| **API error handling** | Structured error responses with Pydantic models |
| **Configuration centralization** | `.env` file for all credentials and settings |
| **Unit tests** | Test files for scraper, loader, API queries |
| **Requirements.txt** | Complete Python dependencies list |

## 🚨 Critical Fixes Applied

### 1. **Missing Channels Added**
```python
# Updated in src/scraper.py
CHANNELS = [
    'lobelia4cosmetics', 'tikvahpharma', 'CheMed123',
    'ethiopharma', 'pharmacyaddis', 'addispharmacy'
]
Complete Data Model
medical_warehouse/models/marts/
├── dim_channels.sql      # Channel dimension ✓
├── dim_dates.sql        # Date dimension ✓ (NEW)
├── fct_messages.sql     # Message facts ✓
└── fct_image_detections.sql # YOLO results ✓
Data Quality Tests
# medical_warehouse/models/marts/schema.yml
tests:
  - unique
  - not_null
  - relationships
  - accepted_values
  - not_negative
 Production-Ready API
# Structured error handling
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return ErrorResponse(
        status="error",
        error="Internal server error",
        details={"type": str(type(exc).__name__)}
    )


\## ✅ All 5 Tasks Completed



\### Task 1: Data Scraping \& Collection ✓

\- `src/scraper.py` - Working Telegram scraper

\- Raw data lake: `data/raw/telegram\_messages/` and `data/raw/images/`

\- 20 messages, 15 images collected



\### Task 2: Data Modeling \& Transformation ✓

\- \*\*PostgreSQL option\*\*: `src/load\_to\_postgres.py`, `docker-compose.yml`

\- \*\*SQLite implementation\*\*: `src/load\_to\_sqlite.py`, `medical\_warehouse.db`

\- \*\*dbt project\*\*: `medical\_warehouse/` with:

&nbsp; - Staging: `stg\_telegram\_messages.sql`

&nbsp; - Star schema: `dim\_channels.sql`, `fct\_messages.sql`

&nbsp; - Tests: `assert\_no\_future\_messages.sql`, `assert\_positive\_views.sql`



\### Task 3: Data Enrichment with YOLO ✓

\- `src/yolo\_detect.py` - Image detection script

\- `data/processed/yolo\_detections.csv` - Detection results

\- `fct\_image\_detections.sql` - Integrated model



\### Task 4: Analytical API with FastAPI ✓

\- `api/main.py` - 5 working endpoints

\- `api/database.py` - Database connection

\- `api/schemas.py` - Pydantic validation

\- \*\*Endpoints\*\*: 

&nbsp; - `/api/summary` - Overall statistics

&nbsp; - `/api/reports/top-products` - Product analysis

&nbsp; - `/api/channels/{channel}/activity` - Channel metrics

&nbsp; - `/api/search/messages` - Message search

&nbsp; - `/api/reports/visual-content` - Image analytics



\### Task 5: Pipeline Orchestration with Dagster ✓

\- `complete\_pipeline.py` - Full orchestration

\- \*\*Ops\*\*: scraping, loading, dbt, YOLO, API

\- \*\*Dagster UI\*\*: http://localhost:3000



\## 🚀 Quick Start

```bash

\# 1. Clone repository

git clone https://github.com/beza1619/medical-telegram-warehouse.git



\# 2. Install dependencies

pip install -r requirements.txt



\# 3. Set up environment

cp .env.example .env

\# Add your Telegram API credentials



\# 4. Run the pipeline

python src/scraper.py

python src/load\_to\_sqlite.py

python src/yolo\_detect.py



\# 5. Start services

python -m uvicorn api.main:app --port 8000

python -m dagster dev -f complete\_pipeline.py --port 3000

📊 Business Insights

Top Products: NIDO, Olive Oil, Vitamin D3+k2



Price Range: 6000-8500 Ethiopian Birr



Visual Content: 75% of posts include images



Engagement: Average 219 views per message



🔗 Live Access

API: http://127.0.0.1:8000



API Docs: http://127.0.0.1:8000/docs

Dagster UI: http://127.0.0.1:3000



📁 Repository Structure

medical-telegram-warehouse/

├── src/                    # Tasks 1 \& 3

├── api/                    # Task 4

├── medical\_warehouse/      # Task 2 (dbt)

├── data/                   # Raw \& processed data

├── notebooks/              # Analysis

├── complete\_pipeline.py    # Task 5 (Dagster)

└── \*.py                    # Supporting scripts

📄 License

MIT License - Academic Project for Kara Solutions



\*\*Push to GitHub and you're done!\*\*

