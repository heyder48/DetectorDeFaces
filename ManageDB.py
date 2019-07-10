
import os
import sqlite3
import io
from decimal import Decimal


class Connect(object):

    def __init__(self, DBname):
        
        try:
            self.conn = sqlite3.connect(DBname)
            self.cursor = self.conn.cursor()

            print("Banco: ",DBname)

            self.cursor.execute('SELECT SQLITE_VERSION()')
            self.data = self.cursor.fetchone()
            print("SQlite version: {}".format(self.data))
        except sqlite3.Error:

            print("Fail to connect to DB")

    def CommitDB(self):
        if self.conn:
            self.conn.commit()
    
    def CloseDB(self):

        if self.conn:
            self.conn.close()
            print("DB Closed.")

class Usuario(object):

    def __init__(self):
        self.db = Connect('Usuario.db')
    
    def CloseConecction(self):

        self.db.CloseDB()
    
    def TemperatureGrab(self,name):

        sqlCommand = "SELECT Temperature FROM Registro WHERE Name  = \'{}\'".format(name )
        Temp = self.db.cursor.execute(sqlCommand)
         
        return Decimal(Temp.fetchone()[0])


    


