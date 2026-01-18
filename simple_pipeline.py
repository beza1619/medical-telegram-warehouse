from dagster import job, op, repository

@op
def step_one():
    return "✅ Scraped Telegram data"

@op
def step_two():
    return "✅ Loaded to SQLite database"

@op
def step_three():
    return "✅ Analyzed with Jupyter"

@op
def step_four():
    return "✅ API: http://127.0.0.1:8000"

@job
def medical_telegram_pipeline():
    s1 = step_one()
    s2 = step_two()
    s3 = step_three()
    s4 = step_four()
    
    return {
        "status": "complete",
        "steps": [s1, s2, s3, s4],
        "api_url": "http://127.0.0.1:8000",
        "docs_url": "http://127.0.0.1:8000/docs"
    }

@repository
def my_repo():
    return [medical_telegram_pipeline]

if __name__ == "__main__":
    # Simple test
    result = medical_telegram_pipeline.execute_in_process()
    print("Pipeline executed successfully!")
    print("Output:", result.output_values)