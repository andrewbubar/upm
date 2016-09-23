#!/usr/bin/python

# Automatically sends data to a file and deletes table

import sqlite3 as lite

with open('backup.csv', 'w+') as write_file
  con = lite.connect('makerspace.db')
  cur = con.cursor()
  for row in cur.execute("SELECT * FROM USED"):
    write_file.write(','.join(row))
    write_file.write('\n')
  cur.execute("DELETE FROM USED")
  con.commit()
  con.close()
