import psycopg2
import os
from persistent.query import QuerySet
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

# Create QuerySet object
qs = QuerySet(connector=conn)

# Sample data
data = { "version_id": "750", "last_updated": str(date(1999, 12, 11)), "active": "True", "gender": "Female"}

# insert sample data to our database server (local)
qs.insert_practitioner(data=data)

# Disconnect
conn.close()