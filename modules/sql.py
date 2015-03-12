import MySQLdb
import pdb

class basketball_db:
        def __init__(self, year):
                self.host = "localhost"
                self.user = "root"
                self.passwd = ""
                self.db_name = str(year)
                try:
                        self.connect = MySQLdb.connect(host=self.host, user=self.user, 
                            passwd=self.passwd, db=self.db_name)
                except Exception as e:        
                        if e[0] == 1049:
                                self.create_database()
                        else:
                                raise e

        def create_database(self):
                try:
                        self.connect = MySQLdb.connect(host=self.host, user=self.user, 
                            passwd=self.passwd)
                except Exception as e:
                        raise e
                if not self.db_name:  
                        raise Exception("Empty database name")
                sql_command = "CREATE DATABASE " + self.db_name
                self.db = self.connect.cursor()
                self.db.execute(sql_command)

        def insert_data(self, data, db_name):
                """data should be in a dictionary format
                which must contain the following attributes
                1. table name
                2. key name
                3. content must be in a list formatt"""

