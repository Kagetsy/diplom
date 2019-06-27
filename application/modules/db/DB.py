import sqlite3

class DB:

    conn = None

    def __init__(self, options):
        self.conn = sqlite3.connect(options['PATH'])
        self.conn.row_factory = self.dictFactory
        self.c = self.conn.cursor()

    def __del__(self):
        self.conn.close()

    def dictFactory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def getUser(self, options):
        query = "SELECT * FROM users WHERE login= ? AND password= ?"
        self.c.execute(query, options)
        return self.c.fetchone()

    def getUserByToken(self, options):
        query = "SELECT * FROM users WHERE token= '" + options + "'"
        self.c.execute(query)
        return self.c.fetchone()

    def updateUserToken(self, options):
        query = 'UPDATE users SET token= ? WHERE id= ?'
        self.c.execute(query, options)
        return self.conn.commit()

    def getCheck(self,options):
        query = "SELECT * FROM check_system"
        self.c.execute(query, options)
        return self.c.fetchone()    