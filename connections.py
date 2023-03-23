import psycopg2 as pg2
import os
from dotenv import load_dotenv

load_dotenv()

database = os.getenv('DatabaseName')
user = os.getenv("UserName")
password = os.getenv("Password")


# def create_connection():
#     """Create a new database connection."""
#     conn = pg2.connect(f"dbname={database} user={user} password={password}"
#     )
#     return conn

# def close_connection(conn):
#     """Close the database connection."""
#     conn.close()

# def create_table():
#     """Create the reports table if it does not exist."""
#     conn = create_connection()
#     cur = conn.cursor()
#     cur.execute(
#         """
#         CREATE TABLE IF NOT EXISTS reports (
#             report_id UUID PRIMARY KEY,
#             status VARCHAR(20)
#         );
#         """
#     )
#     conn.commit()
#     cur.close()
#     close_connection(conn)

# def insert_report(report_id):
#     """Insert a new report with the specified ID and status 'running'."""
#     conn = create_connection()
#     cur = conn.cursor()
#     cur.execute(
#         """
#         INSERT INTO reports (report_id, status) VALUES (%s, %s);
#         """,
#         (report_id, 'running')
#     )
#     conn.commit()
#     cur.close()
#     close_connection(conn)

# def update_report(report_id, status):
#     """Update the status of a report with the specified ID."""
#     conn = create_connection()
#     cur = conn.cursor()
#     cur.execute(
#         """
#         UPDATE reports SET status = %s WHERE report_id = %s;
#         """,
#         (status, report_id)
#     )
#     conn.commit()
#     cur.close()
#     close_connection(conn)

# def get_report_status(report_id):
#     """Retrieve the status of a report with the specified ID."""
#     conn = create_connection()
#     cur = conn.cursor()
#     cur.execute(
#         """
#         SELECT status FROM reports WHERE report_id = %s;
#         """,
#         (report_id,)
#     )
#     result = cur.fetchone()
#     cur.close()
#     close_connection(conn)
#     return result[0] if result else None

def create_connection():
    conn = pg2.connect(f"dbname={database} user={user} password={password}")
    cursor = conn.cursor()
    return cursor


def fetch_result(query: str):
    cursor = create_connection()
    cursor.execute(query)
    return cursor.fetchone()

def close_conn(conn, cur):
    # Commit the transaction
    conn.commit()
    cur.close()
    conn.close()


# if __name__ == "__main__":
#     result = fetch_result("select * from store_status")
#     print(result)

