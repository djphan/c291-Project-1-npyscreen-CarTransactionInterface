import cx_Oracle
import npyscreen

class Database:
    def __init__(self, connect_str):
        try:
            self.connection = cx_Oracle.connect(connect_str)
            self.cursor = self.connection.cursor()
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args 
            npyscreen.notify_confirm(error.message, editw=1,
                                                    title='Login failure')

            # PUT IN NULL PROCESSING
            # if self.entries[field] in {'', 'null'}: # If the entry is blank fill in null
            #     self.entries[field] = 'null'

    def insert(self, values_dict, prepare_statement):
        self.cursor.prepare(prepare_statement.upper()) # prepare cursor
        try:
            # subsitute dictionary values and execute SQL
            self.cursor.setinputsizes(image=cx_Oracle.BLOB)
            self.cursor.execute(None, {i:values_dict[i].upper() for i in values_dict}) 
        except cx_Oracle.DatabaseError as exc:
            # return error arguments if an error occurs, else return None
            error = exc.args[0]
            return error
        else:
            self.connection.commit()

    def query(self, values_dict, prepare_statement):
        self.cursor.prepare(prepare_statement) # prepare cursor
        try:
            # subsitute dictionary values and execute SQL
            self.cursor.execute(None, values_dict) 
        except cx_Oracle.DatabaseError as exc:
            # return error arguments if an error occurs, else return None
            error = exc.args[0]
            return error
        # if TitleTextno error, then return the database results
        rv = self.cursor.fetchall()
        return rv

    def delete(self, values_dict, prepare_statement):
        self.cursor.prepare(prepare_statement) # prepare cursor
        try:
            # subsitute dictionary values and execute SQL
            self.cursor.execute(None, values_dict) 
        except cx_Oracle.DatabaseError as exc:
            # return error arguments if an error occurs, else return None
            error = exc.args[0]
            return error
        else:
            self.connection.commit()
        return rv
