"""Quick query script for looking up DB values."""
import sqlite3

DB_CONFIG = open("db_config", "r").read()
con = sqlite3.connect(DB_CONFIG)
cur = con.cursor()
cur.execute("select * from authors")
print(cur.fetchone())
