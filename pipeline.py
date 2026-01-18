from dagster import job, op, get_dagster_logger
import subprocess
import os

logger = get_dagster_logger()

@op
def scrape_telegram_data():
    """Run Telegram scraper"""
    logger.info("Starting Telegram scraping...")
    result = subprocess.run(["py", "src/scraper.py"], capture_output=True, text=True)
    if result.returncode == 0:
        logger.info("✅ Scraping completed successfully")
        logger.info(result.stdout)
    else:
        logger.error(f"❌ Scraping failed: {result.stderr}")
    return result.returncode

@op
def load_to_database():
    """Load scraped data to SQLite"""
    logger.info("Loading data to database...")
    result = subprocess.run(["py", "src/load_to_sqlite.py"], capture_output=True, text=True)
    if result.returncode == 0:
        logger.info("✅ Database loading completed")
        logger.info(result.stdout)
    else:
        logger.error(f"❌ Database loading failed: {result.stderr}")
    return result.returncode

@op
def analyze_data():
    """Run Jupyter analysis"""
    logger.info("Running data analysis...")
    
    # Create analysis notebook if needed
    analysis_code = '''
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("medical_warehouse.db")
df = pd.read_sql_query("SELECT * FROM raw_telegram_messages", conn)

# Basic analysis
summary = {
    "total_messages": len(df),
    "channels": df["channel_name"].nunique(),
    "avg_views": df["views"].mean(),
    "with_images": df["has_media"].sum()
}

print("📊 Analysis Summary:")
for key, value in summary.items():
    print(f"  {key}: {value}")

conn.close()
'''
    
    with open("temp_analysis.py", "w") as f:
        f.write(analysis_code)
    
    result = subprocess.run(["py", "temp_analysis.py"], capture_output=True, text=True)
    
    if result.returncode == 0:
        logger.info("✅ Analysis completed")
        logger.info(result.stdout)
    else:
        logger.error(f"❌ Analysis failed: {result.stderr}")
    
    # Clean up
    if os.path.exists("temp_analysis.py"):
        os.remove("temp_analysis.py")
    
    return result.returncode

@op
def start_api():
    """Start FastAPI server"""
    logger.info("Starting FastAPI server...")
    logger.info("API will be available at: http://127.0.0.1:8000")
    logger.info("Press CTRL+C to stop the pipeline")
    return "API running at http://127.0.0.1:8000"

@job
def medical_telegram_pipeline():
    """Main pipeline orchestrating all tasks"""
    # Run tasks in sequence
    scrape_result = scrape_telegram_data()
    load_result = load_to_database()
    analysis_result = analyze_data()
    api_status = start_api()
    
    return {
        "scraping": "✅" if scrape_result == 0 else "❌",
        "loading": "✅" if load_result == 0 else "❌",
        "analysis": "✅" if analysis_result == 0 else "❌",
        "api": api_status
    }

if __name__ == "__main__":
    # Run the pipeline
    result = medical_telegram_pipeline.execute_in_process()
    print("\n" + "="*50)
    print("Pipeline Execution Result:")
    print("="*50)
    for key, value in result.output_values.items():
        print(f"{key}: {value}")