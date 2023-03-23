from fastapi import FastAPI
# from schema import Report, ReportStatus
from generate_report import generate_report
import asyncio
import time
import uuid
import uvicorn
from ..connections import create_connection, fetch_result, close_conn

app = FastAPI()



tasks = {}

def long_running_task(cur, report_id):
    time.sleep(60)
    cur.execute("INSERT INTO reports (report_id, status) VALUES (%s, %s)", (report_id, "running"))
    return "Task completed"

@app.post("/trigger_report")
async def start_task():
    # Generate a unique task ID
    report_id = str(uuid.uuid4())

    # Start the task in the background
    loop = asyncio.get_running_loop()
    cur  = create_connection()
    report = loop.run_in_executor(None, lambda: long_running_task(cur, report_id))

    # Store the task in a dictionary so we can retrieve it later
    tasks[report_id] = report

    # Return the task ID
    return {"task_id": report_id}

@app.get("/get_report/{report_id}")
async def get_task_status(report_id: str):
    if report_id not in tasks:
        return {"error": "Invalid task ID"}

    if tasks[report_id].done():
        # If the task is done, return the result
        result = tasks[report_id].result()
        return {"status": "completed", "result": result}
    else:
        # If the task is still running, return the status
        return {"status": "running"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)