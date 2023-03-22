from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import random

app = FastAPI()

class Report(BaseModel):
    report_id: Optional[str]
    
class ReportStatus(BaseModel):
    status: str
    csv: Optional[str]

@app.get("/trigger_report")
async def trigger_report():
    # Code to generate report ID and start report generation process
    report_id = str(random.randint(10000000, 99999999))
    # Code to start report generation process using database
    return {"report_id": report_id}

@app.post("/get_report/{report_id}")
async def get_report(report_id: int, report: Report):
    # Code to check report generation status using report ID
    # If report is still running, return status "Running"
    # If report is complete, return status "Complete" and CSV with report data
    # The CSV can be returned as a string or file path depending on your implementation
    return {"status": "Running", "csv": None}