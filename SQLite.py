import sqlite3

class SQLite:
    def __init__(self, db:str):
        self.db = db
        self.connection = sqlite3.connect(db)
        self.cursor = self.connection.cursor()

    def execute(self, command:str):
        return self.cursor.execute(command)
    
    def tableExists(self, table:str):
        query = f"""SELECT name FROM sqlite_master WHERE type='table' AND name='{table}';"""
        result = self.execute(query)
        if(result.fetchone()):
            return True
        else:
            return False

    def commit(self):
        self.connection.commit()

    def __del__(self):
        self.connection.close()
