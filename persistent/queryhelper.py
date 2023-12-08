# Author: Imgyeong Lee
# Last updated: 08 December 2023

# TODO: NEED TO ADD AND CHECK CONSTRAINTS
# TODO: NEED TO DEAL WITH a join table of pracitioner_role and taxonomy

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


# Checklist for text[] type
PRACTITIONER_ARRAY_CHECKLIST = ["name_given"]


"""
QueryHelper class
Support: SELECT, INSERT
"""
# QueryHelper class
# Support: SELECT, INSERT
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

    """
    Return the result of SELECT * query execution
    :param tableName(string)
    :return [tuple]
    """
    def fetch_all(self, tableName):
        query = f"{_SELECT_ALL} {SCHEMA_NAME}.{tableName}"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    """
    Return a specific number of the result of SELECT * query execution
    :param tableName(string)
    :return [tuple]
    """
    def fetch_many(self, tableName, size):
        query = f"{_SELECT_ALL} {SCHEMA_NAME}.{tableName}"
        self.cursor.execute(query)
        return self.cursor.fetchmany(size=size)

    """
    Return a one of the result of SELECT * query execution
    :param tableName(string)
    :return tuple
    """
    def fetch_one(self, tableName):
        query = f"{_SELECT_ALL} {SCHEMA_NAME}.{tableName}"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def fetch_specific(self, tableName, data, single=False):
        query = f"SELECT * FROM {SCHEMA_NAME}.{tableName} WHERE "
        condition = ""
        if tableName == "practitioner":
            name_given = data["given_name"]
            name_family = data["family_name"]
            npi = data["npi"]
            condition += f"{name_given}=ANY(name_given) "
            condition += f"AND name_family={name_family} "
            condition += f"AND npi={npi} "

        query += condition

        self.cursor.execute(query)

        if single:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()


    """
    Close the connection to the database server
    """
    def disconnect(self):
        self.cursor.close()
        self.connector.close()

    """
    Get the validation checklist by a given type
    :param type(string)
    :return list
    """
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

    def get_arraylist(self, type):
        if type == "practitioner":
            return PRACTITIONER_ARRAY_CHECKLIST
        else:
            print("❌ ERROR: get_checklist DOES NOT FIND ANY MATCHED TYPE.\n")
            return []

    """
    Get the table name by a given type
    :param type(string)
    :return string
    """
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
            return ""

    """
    Parse the data by a given type
    :param type(string)
    :param data(dictionary)
    :return tuple
    """
    def parse_data(self, type, data):
        checklist = self.get_checklist(type)
        arraylist = self.get_arraylist(type)

        if len(checklist) == 0:
            print("❌ ERROR: parse_data HAS AN EMPTY ARRAY.\n")

        parsed_data = []
        for data_value in checklist:
            if data_value in data:
                if data_value in arraylist:
                    parsed_data.append([data[data_value]])
                else:
                    parsed_data.append(data[data_value])
            else:
                parsed_data.append(None)

        input = tuple(parsed_data)
        return input

    """
    Create an INSERT query by a given type
    :param type(string)
    :return string
    """
    def create_insert_query(self, type):
        table = self.get_table(type)
        checklist = self.get_checklist(type)
        if len(checklist) < 1:
            return

        values = "%s, " * (len(checklist) - 1) + "%s"
        table_list = ", ".join(checklist)
        insert_query = f"INSERT INTO {table} ({table_list}) VALUES ({values});"

        return insert_query

    """
    Execute insert query.
    :param type(string)
    :param data(dictionary)
    """
    def insert(self, type, data):
        insert_query = self.create_insert_query(type)
        parsed_input = self.parse_data(type, data)
        self.cursor.execute(insert_query, parsed_input)
        self.connector.commit()

