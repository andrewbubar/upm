#!/usr/bin/python

import sqlite3 as lite

con = lite.connect('makerspace.db')

test = (("1234567890", 'Test', 'Test', 'Test'))

with con:
  cur = con.cursor()
  cur.execute("DROP TABLE IF EXISTS USED")
  cur.execute("CREATE TABLE USED(ID TEXT, Name TEXT, TimeStart BLOB, TimeStop BLOB)")
  cur.execute("INSERT INTO USED VALUES(?,?,?,?)", test)

con.commit()
con.close()
