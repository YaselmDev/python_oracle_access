import cx_Oracle


class OracleAccess:
    def __init__(self, user, password, server, port, sid):
        """
        Initialize the DB connection
        :param user:
        :param password:
        :param server:
        :param port:
        :param sid:
        """
        self.tns = cx_Oracle.makedsn(server, port, sid)
        self.connection = None
        self.cursor = None
        self.user = user
        self.password = password
        print("OracleAccess - Connection initialized: ", sid)

    def connect(self):
        """
        Open the DB connection - Catch the exception if database error
        :return:
        """
        try:
            self.connection = cx_Oracle.connect(self.user, self.password, self.tns)
            self.cursor = self.connection.cursor()
            print("OracleAccess - Connection successful.")
        except cx_Oracle.DatabaseError as e:
            print("OracleAccess - Connection failed: {}".format(e))

    def close(self):
        """
        Close the DB connection
        :return:
        """
        try:
            self.cursor.close()
            self.connection.close()
        except cx_Oracle.DatabaseError:
            pass
        print("OracleAccess - Connection closed.")

    @staticmethod
    def init_db(json_db):
        """
        Initialize the DB connection from a JSON object
        :param json_db:
        :return: OracleAccess object
        """
        return OracleAccess(json_db['USER'], json_db['PASSWORD'], json_db['SERVER'], json_db['PORT'], json_db['SID'])


# Example of OracleAccess class usage
json_db_config = {"USER": "user", "PASSWORD": "password", "SERVER": "server", "PORT": 1535, "SID": "SID"}
db = OracleAccess.init_db(json_db_config)
db.connect()
db.cursor.execute("SELECT username, city, address FROM person")
# Read the content of the cursor
for row in db.cursor:
    print('Record {0}, {1}, {2}'.format(row[0], row[1], row[2]))
db.close()
