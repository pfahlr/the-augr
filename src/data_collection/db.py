import sqlite3

class sqliteDB:
  def __init__(self, dbfile):
    self.con = sqlite3.connect(dbfile)
    self.cur = self.con.cursor()

  def __del__(self):
    self.con.close()

  def query(self, sql):
    self.cur.execute(sql)

  def commit(self):
    self.con.commit()

  def select_many(self, sql):
    data = []
    for row in cur.execute(sql):
      data.append(row)
    return data

  def select_one(self, sql):
    res = self.cur.execute(sql)
    data = res.fetchone()
    return data

  def insert_one(self, sql, data):
    self.cur.execute(sql, data)
    self.con.commit()

  def insert_many(self, sql, data):
    self.cur.executemany(sql, data)
    self.con.commit()

  