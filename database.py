import cx_Oracle

class Database:
    def __init__(self, connect_str):
        self.connection = cx_Oracle.connect(connect_str)
        self.cursor = self.connection.cursor()

    def insert(self, values_dict, prepare_statement):
        self.cursor.prepare(prepare_statement) # prepare cursor
        try:
            # subsitute dictionary values and execute SQL
            self.cursor.execute(None, values_dict) 
        except cx_Oracle.DatabaseError as exc:
            # return error arguments if an error occurs, else return None
            error = exc.args
            return error

    def query(self, values_dict, prepare_statement):
        self.cursor.prepare(prepare_statement) # prepare cursor
        try:
            # subsitute dictionary values and execute SQL
            self.cursor.execute(None, values_dict) 
        except cx_Oracle.DatabaseError as exc:
            # return error arguments if an error occurs, else return None
            error = exc.args
            return error
        # if no error, then return the database results
        rv = self.cursor.fetchall()
        return rv

