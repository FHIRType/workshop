# Author: Imgyeong Lee
# Date: 21 November 2023
# Description: Class for queries

_SELECT_ALL = "SELECT * FROM "
PRACTITIONER_TABLE = "fhirtype.practitioner"
class QuerySet:
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

    def parse_pracitioner_data(self, data):
        parsed_data = []

        if "version_id" in data:
            parsed_data.append(data["version_id"])
        if "last_updated" in data:
            parsed_data.append(data["last_updated"])

        if "active" in data:
            parsed_data.append(data["active"])
        else:
            parsed_data.append(None)

        if "gender" in data:
            parsed_data.append(data["gender"])
        else:
            parsed_data.append(None)

        if "name_use" in data:
            parsed_data.append(data["name_use"])
        else:
            parsed_data.append(None)

        if "name_family" in data:
            parsed_data.append(data["name_family"])
        else:
            parsed_data.append(None)

        if "name_given" in data:
            parsed_data.append(data["name_given"])
        else:
            parsed_data.append(None)

        if "name_full" in data:
            parsed_data.append(data["name_full"])
        else:
            parsed_data.append(None)

        input = tuple(parsed_data)
        return input

    def insert_practitioner(self, data):
        insert_query = f"""
            INSERT INTO {PRACTITIONER_TABLE} (version_id, last_updated, active, gender, name_use, name_family, name_given, name_full)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
        """
        parsed_input = self.parse_pracitioner_data(data)
        self.cursor.execute(insert_query, parsed_input)
        self.connector.commit()

