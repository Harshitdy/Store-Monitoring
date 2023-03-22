import psycopg2 as pg2
import os
from dotenv import load_dotenv

load_dotenv()

database = os.getenv('DatabaseName')
user = os.getenv("UserName")
password = os.getenv("Password")

def create_connection():
    conn = pg2.connect(f"dbname={database} user={user} password={password}")
    cursor = conn.cursor()
    return cursor


def fetch_result(query: str):
    cursor = create_connection()
    cursor.execute(query)
    return cursor.fetchone()



if __name__ == "__main__":
    result = fetch_result("select * from store_status")
    print(result)

