# Author: Imgyeong Lee
# Last updated: 22 November 2023
# Description: Class for queries

# TODO: ADD CONSTRAINTS!!!!!!!!!!
# TODO: DEAL WITH a join table of pracitioner_role and taxonomy!!!!!!!!!

# Setting
SCHEMA_NAME="fhirtype"

# Query
_SELECT_ALL = "SELECT * FROM "

# Table names
IDENTIFIER_TABLE = f"{SCHEMA_NAME}.identifier"
LOCATION_TABLE = f"{SCHEMA_NAME}.location"
ORGANIZATION_TABLE = f"{SCHEMA_NAME}.organization"
PRACTITIONER_TABLE = f"{SCHEMA_NAME}.practitioner"
PRACTITIONER_ROLE_TABLE = f"{SCHEMA_NAME}.practitioner_role"
TAXONOMY_TABLE = f"{SCHEMA_NAME}.taxonomy"

# Checklist for each table
PRACTITIONER_CHECKLIST = ["version_id", "last_updated", "active", "gender", "name_use", "name_family", "name_given", "name_full"]
IDENTIFIER_CHECKLIST = ["code", "display", "system", "value", "use"]
LOCATION_CHECKLIST = ["version_id", "last_updated", "status", "name", "phone_number", "fax_number", "longitude", "latitude", "address_line", "address_city", "address_state", "postal_code"]
ORGANIZATION_CHECKLIST = ["version_id", "last_updated", "status", "name", "phone_number", "fax_number", "longitude", "latitude", "address_line", "address_city", "address_state", "postal_code"]
PRACTITIONER_ROLE_CHECKLIST = ["version_id", "last_updated", "active"]
TAXONOMY_CHECKLIST = ["code", "display", "system"]


class QueryHelper:
    def __init__(self, connector):
        self.connector = connector
        self.cursor = connector.cursor()

    def set_connector(self, connector):
        self.connector = connector

    def set_cursor(self, cursor):
        self.cursor = cursor

    def get_connector(self):
        return self.connector

    def get_cursor(self):
        return self.cursor

    def fetch_all(self, tableName):
        query = _SELECT_ALL + tableName
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def fetch_many(self, tableName, size):
        query = _SELECT_ALL + tableName
        self.cursor.execute(query)
        return self.cursor.fetchmany(size=size)

    def fetch_one(self, tableName):
        query = _SELECT_ALL + tableName
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def disconnect(self):
        self.cursor.close()
        self.connector.close()

    def get_checklist(self, type):
        if type == "practitioner":
            return PRACTITIONER_CHECKLIST
        elif type == "identifier":
            return IDENTIFIER_CHECKLIST
        elif type == "location":
            return LOCATION_CHECKLIST
        elif type == "pracitioner_role":
            return PRACTITIONER_ROLE_CHECKLIST
        elif type == "organization":
            return ORGANIZATION_CHECKLIST
        elif type == "taxonomy":
            return TAXONOMY_CHECKLIST
        else:
            print("❌ ERROR: get_checklist DOES NOT FIND ANY MATCHED TYPE.\n")
            return []

    def get_table(self, type):
        if type == "practitioner":
            return PRACTITIONER_TABLE
        elif type == "identifier":
            return IDENTIFIER_TABLE
        elif type == "location":
            return LOCATION_TABLE
        elif type == "pracitioner_role":
            return PRACTITIONER_ROLE_TABLE
        elif type == "organization":
            return ORGANIZATION_TABLE
        elif type == "taxonomy":
            return TAXONOMY_TABLE
        else:
            print("❌ ERROR: get_table DOES NOT FIND ANY MATCHED TYPE.\n")
            return []

    def parse_data(self, type, data):
        checklist = self.get_checklist(type)

        if len(checklist) == 0:
            print("❌ ERROR: parse_data HAS AN EMPTY ARRAY.\n")

        parsed_data = []
        for data_value in checklist:
            if data_value in data:
                parsed_data.append(data[data_value])
            else:
                parsed_data.append(None)

        input = tuple(parsed_data)
        return input

    def create_insert_query(self, type):
        table = self.get_table(type)
        checklist = self.get_checklist(type)
        if len(checklist) < 1:
            return

        values = "%s, " * (len(checklist) - 1) + "%s"
        table_list = ", ".join(checklist)
        insert_query = f"INSERT INTO {table} ({table_list}) VALUES ({values});"

        return insert_query

    def insert(self, type, data):
        insert_query = self.create_insert_query(type)
        parsed_input = self.parse_data(type, data)
        self.cursor.execute(insert_query, parsed_input)
        self.connector.commit()

