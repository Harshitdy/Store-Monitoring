import psycopg2
import uuid
import time
from fastapi import FastAPI, Response
from urllib.parse import quote_plus
from sqlalchemy import text
import asyncio
from dotenv import load_dotenv
import pandas as pd
from io import StringIO
import uvicorn
import os
from sqlalchemy import create_engine

database = os.getenv('DatabaseName')
username = os.getenv("UserName")
password = os.getenv("Password")

engine = create_engine(f"postgresql+psycopg2://{username}:%s@localhost/{database}" % quote_plus(f"{password}"))

tasks = {}

load_dotenv()


# Connect to the PostgreSQL database
def create_conn():
    conn = psycopg2.connect(
        database=database,
        user=username,
        password=password
    )
    return conn


# Initialize the FastAPI app
app = FastAPI()

# Define the long-running task function
def long_running_task(report_id):
    time.sleep(60)
    # Connect to the PostgreSQL database
    conn = create_conn()

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Update the status of the task in the database
    cur.execute("UPDATE reports_db SET status = %s WHERE report_id = %s", ("completed", report_id))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

    return "Task completed"

# Define the endpoint to start the task
@app.post("/trigger_report")
async def start_task():
    # Generate a unique task ID
    report_id = str(uuid.uuid4())

    # Connect to the PostgreSQL database
    conn = create_conn()

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Insert the task into the database
    cur.execute("INSERT INTO reports_db (report_id, status) VALUES (%s, %s)", (report_id, "running"))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Start the task in the background
    loop = asyncio.get_running_loop()
    report = loop.run_in_executor(None, long_running_task, report_id)

    # Connect to the PostgreSQL database
    conn = create_conn()

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Update the status of the task in the database
    cur.execute("UPDATE reports_db SET status = %s WHERE report_id = %s", ("running", report_id))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cur.close()
    conn.close()

    # Store the task in a dictionary so we can retrieve it later
    tasks[report_id] = report

    # Return the task ID
    return {"task_id": report_id}

# Define the endpoint to get the task status
@app.get("/get_report/{report_id}")
async def get_task_status(report_id: str, response: Response):
    # Connect to the PostgreSQL database
    conn = create_conn()

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Retrieve the status of the task from the database
    cur.execute("SELECT status FROM reports_db WHERE report_id = %s", (report_id,))
    row = cur.fetchone()

    # If the task ID is invalid, return an error
    if row is None:
        cur.close()
        conn.close()
        return {"error": "Invalid task ID"}

    status = row[0]

    # If the task is running, return the status
    if status == "running":
        cur.close()
        conn.close()
        return {"status": "running"}

    # If the task is completed, retrieve the result from the dictionary
    if status == "completed":

        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM store_business_hours LIMIT 10"))
            # Create a CSV file
            csv_string = StringIO()
            headers = [column[0] for column in result.cursor.description]
            csv_string.write(','.join(headers) + '\n')
            for row in result:
                csv_string.write(','.join(str(value) for value in row) + '\n')
            # Set the content type and disposition headers to trigger the download
            response.headers["Content-Type"] = "text/csv"
            response.headers["Content-Disposition"] = f"attachment; filename=results_{report_id}.csv"
            # Return the CSV file as a response
            return Response(content=csv_string.getvalue(), media_type="text/csv")

if __name__ == "__main__":
    uvicorn.run("test:app", host="0.0.0.0", port=8000, reload=True)
