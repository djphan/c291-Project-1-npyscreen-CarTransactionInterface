import cx_Oracle
import npyscreen

class Database:
    """
    Holds a cx_Oracle database connection and cursor. Defines a standard insert
    method and query method to be used by all forms on MyApplication.

    Instances of this class are intended to be assigned to MyApplication.db,
    such that any form may access its methods by calling on self.parentApp.db.
    """

    def __init__(self, connect_str=None):
        if connect_str is None:
            self.logged_in = False
            return
        try:
            self.connection = cx_Oracle.connect(connect_str)
        except cx_Oracle.DatabaseError as exc:
            error, = exc.args 
            self.logged_in = False
            npyscreen.notify_confirm(error.message, editw=1,
                                                    title='Login failure')
            raise exc
        else:
            self.cursor = self.connection.cursor()
            self.logged_in = True

    def insert(self, values_dict, prepare_statement):
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

    def query(self, values_dict, prepare_statement):
        self.cursor.prepare(prepare_statement) # prepare cursor
        try:
            # subsitute dictionary values and execute SQL
            self.cursor.execute(None, values_dict) 
        except cx_Oracle.DatabaseError as exc:
            # return error arguments if an error occurs, else return None
            error = exc.args[0]
            return error
        rv = self.cursor.fetchall()
        return rv

    # The delete method currently does the same as insert, so this ensures that
    # changes to insert affect delete as well
    delete = insert
