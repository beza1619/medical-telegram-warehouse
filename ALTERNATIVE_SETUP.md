\# Alternative Setup (Using SQLite)



Since PostgreSQL installation had issues, this project uses SQLite which is built into Python.



\## Working Components:



1\. \*\*Data Storage\*\*: `medical\_warehouse.db` (SQLite database)

2\. \*\*Scraper\*\*: `src/scraper.py` ✓ Working

3\. \*\*Loader\*\*: `src/load\_to\_sqlite.py` ✓ Working  

4\. \*\*API\*\*: `api/main.py` ✓ Working (5 endpoints)

5\. \*\*Analysis\*\*: `notebooks/analysis.ipynb` ✓ Working

6\. \*\*Orchestration\*\*: `test\_pipeline.py` ✓ Working (Dagster)



\## To Add PostgreSQL Later:



1\. Install PostgreSQL from https://www.postgresql.org/download/windows/

2\. Use password: `telegram\_pass`, port: `5432`

3\. Run `setup\_postgres.sql` in pgAdmin

4\. Update `.env` with PostgreSQL credentials

5\. Use `src/load\_to\_postgres.py` instead of SQLite loader

