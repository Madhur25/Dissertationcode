import pyodbc
class MetaSingleton(type):
    _instances ={}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=MetaSingleton):
    connection =None
    def connect(self):
        if self.connection is None:
            self.connection =pyodbc.connect('Driver=ODBC Driver 17 for SQL Server;'
                      'Server=servername;'
                      'Dao=mscdissertation;'
                      'Trusted_Connection=yes;')
            self.cursorobj = self.connection.cursor()
        return self.cursorobj
