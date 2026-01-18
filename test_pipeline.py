from dagster import Definitions, job, op, Out

@op(out=Out(str))
def hello():
    return "Pipeline works!"

@job
def test_job():
    hello()

defs = Definitions(jobs=[test_job])

if __name__ == "__main__":
    result = test_job.execute_in_process()
    print("✅ Success!")