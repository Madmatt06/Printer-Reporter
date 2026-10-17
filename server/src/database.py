import sqlite3

class Database:
  def __init__(self, database_file:str):
    self.conn:sqlite3.Connection = sqlite3.connect(database_file)
    self.cursor:sqlite3.Cursor = self.conn.cursor()
    #self.cursor.execute("CREATE TABLE IF NOT EXISTS printers_table (id INTEGER PRIMARY KEY AUTOINCREMENT, ...);")