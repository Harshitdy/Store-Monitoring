from pydantic import BaseModel
from typing import Optional

# class Report(BaseModel):
#     report_id: Optional[str]
    
# class ReportStatus(BaseModel):
#     status: str
#     csv: Optional[str]

class ReportData(BaseModel):
    store_id: str
    uptime_last_hour: int
    uptime_last_day: int
    uptime_last_week: int
    downtime_last_hour: int
    downtime_last_day: int
    downtime_last_week: int
