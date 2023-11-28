import psycopg2
import os
from persistent.queryhelper import QueryHelper
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
qs = QueryHelper(connector=conn)
print(qs.fetch_one("practitioner"))

# Sample data
data = { "version_id": "907", "last_updated": str(date(2023, 11, 22)), "active": "True", "gender": "Female"}

# insert sample data to our database server (local)
qs.insert(type="practitioner", data=data)

# Disconnect
conn.close()