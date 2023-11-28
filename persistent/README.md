# Persistence Layer
This section is for the jobs related to our database.
## QueryHelper
QueryHelper class is in queryhelper .py file. You can see how to use that class for your query execution via main.py file under /persistent.
## Setup instruction (Local server)
1. Install all required Python modules in `requirements.txt`.
2. Install PostgreSQL with PgAdmin 4.
3. Complete the basic setup of PgAdmin.
4. You will need to create your schema with the name, `fhirtype`
5. Open the PgAdmin and copy & paste the DDL.sql material into the query editor.
6. Create your `.env` file. (You can see the sample via `.env.sample`)