from schema import ReportData
import csv


# Define a dictionary to store reports
reports = {}

# Define a function to generate a report
def generate_report(report_id):
    # Query the database and get the report data
    # In this example, we'll just create some dummy data
    report_data = [
        ReportData(store_id="Store 1", uptime_last_hour=50, uptime_last_day=600, uptime_last_week=3600,
                   downtime_last_hour=10, downtime_last_day=120, downtime_last_week=720),
        ReportData(store_id="Store 2", uptime_last_hour=45, uptime_last_day=540, uptime_last_week=3240,
                   downtime_last_hour=15, downtime_last_day=180, downtime_last_week=1080),
        ReportData(store_id="Store 3", uptime_last_hour=60, uptime_last_day=720, uptime_last_week=4320,
                   downtime_last_hour=5, downtime_last_day=60, downtime_last_week=360),
    ]

    # Write the report data to a CSV file
    with open(f"{report_id}.csv", "w", newline="") as csvfile:
        fieldnames = ["store_id", "uptime_last_hour", "uptime_last_day", "uptime_last_week", "downtime_last_hour", "downtime_last_day", "downtime_last_week"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for data in report_data:
            writer.writerow(data.dict())

    # Update the report status
    reports[report_id] = "Complete"