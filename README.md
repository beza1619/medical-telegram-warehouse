\# Medical Telegram Warehouse Pipeline



End-to-end data pipeline for Ethiopian medical Telegram channels analysis.



\## 🏗️ Architecture

Telegram → Scraper → SQLite → Analysis → FastAPI → Dagster



\## 📋 Features

\- \*\*Telegram Scraping\*\*: Extract messages/images from Ethiopian medical channels

\- \*\*Data Warehouse\*\*: SQLite database with structured schema

\- \*\*Product Analysis\*\*: Price extraction, trend analysis, insights

\- \*\*FastAPI\*\*: 5 analytical endpoints for business intelligence

\- \*\*Orchestration\*\*: Dagster pipeline for automation



\## 🚀 Quick Start

```bash

\# 1. Clone repository

git clone https://github.com/beza1619/medical-telegram-warehouse.git

cd medical-telegram-warehouse



\# 2. Install dependencies

pip install -r requirements.txt



\# 3. Set up environment

copy .env.example .env

\# Add Telegram API credentials



\# 4. Run pipeline

python src/scraper.py

python src/load\_to\_sqlite.py



\# 5. Start API

python -m uvicorn api.main:app --reload



\# 6. Open Jupyter for analysis

jupyter notebook notebooks/analysis.ipynb

📊 API Endpoints

GET / - API homepage



GET /api/summary - Overall data summary



GET /api/reports/top-products - Most mentioned products



GET /api/channels/{channel}/activity - Channel statistics



GET /api/search/messages?query=... - Message search



GET /api/reports/visual-content - Image usage analysis

🔍 Key Insights

Price Range: 6000-8500 Birr for medical products



Top Products: NIDO, Olive Oil, Vitamin D3+k2



Visual Content: 75% of posts include images



Engagement: Average 219 views per message



🛠️ Tech Stack

Python, Telethon, SQLite, FastAPI, Dagster



Jupyter for analysis, pandas for data processing

📁 Project Structure

medical-telegram-warehouse/

├── src/              # Scraping and data loading

├── api/              # FastAPI application

├── notebooks/        # Jupyter analysis

├── data/             # Raw and processed data

├── medical\_warehouse/# dbt project (planned)

└── tests/            # Unit tests

📄 License

MIT



2\. \*\*Create final report outline\*\* (for Medium-style blog post)



\*\*Your project is complete and on GitHub! Ready for submission.\*\*



