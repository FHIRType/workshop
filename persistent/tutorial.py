import psycopg2
import os
from dotenv import load_dotenv
from datetime import date

# Load envrionment variables (.env)
load_dotenv()

# Connect to the database server (local)
conn = psycopg2.connect(database=os.getenv("DATABASE"),
                        host=os.getenv("HOST"),
                        user=os.getenv("USER"),
                        password=os.getenv("PASSWORD"),
                        port=os.getenv("PORT"))

# create a cursor object to execute any queries on the database
cursor = conn.cursor()

# Execute certain query
cursor.execute("SELECT * FROM practitioner")

# fetchone() - Return one row (the first row) after the SQL query execution.
print(cursor.fetchone())
# fetchall() - Return all rows after the SQL query execution.
print(cursor.fetchall())
# fetchmany() - Return {size} rows after the SQL query execution.
print(cursor.fetchmany(size=5))

# sample insert query for practitioner
insert_query = """
    INSERT INTO practitioner (version_id, last_updated, active, gender)
    VALUES (%s, %s, %s, %s);
"""

last_updated_date = date(2022, 12, 25)

# Execute the query
cursor.execute(insert_query, (2345, last_updated_date, False, 'Female'))

# Apply the changes to our database server
conn.commit()

# Disconnect
cursor.close()
conn.close()