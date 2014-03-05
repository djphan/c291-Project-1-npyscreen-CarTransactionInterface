import cx_Oracle

class Database:
    def __init__(self, connect_str):
        self.connection = cx_Oracle.connect(connect_str)
        self.cursor = self.connection.cursor()

    def insert(self, values_dict, prepare_statement):
        # curs.pre
        # {tablename:x, ncol: x, tablevalues: tuple()}

        return database_response

    def query(self, query_str):
        return response
