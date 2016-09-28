#!/usr/bin/python
import sqlite3 as lite

con = lite.connect('makerspace.db') # connect to makerspace database

people = (
	("9621023222", 'Andrew Bubar', 'Y', 'Y', 'Y'),
        ("321143517", 'Hunter Pickett', 'N', 'N', 'N'),
        )
test = (("1234567890", 'Test', 'Test', 'Test'))

with con:
	cur = con.cursor() # set cursor
	
	# Drop table Permissions, recreate it, add values to it
	cur.execute("DROP TABLE IF EXISTS PERMISSIONS")
	cur.execute("CREATE TABLE PERMISSIONS(ID TEXT, Name TEXT, Laser TEXT, Printer TEXT, Solder TEXT)")
    	cur.executemany("INSERT INTO Permissions VALUES(?,?,?,?,?)",people)
	
	# Drop table Used, recreate it, add values to it
	cur.execute("DROP TABLE IF EXISTS USED")
	cur.execute("CREATE TABLE USED(ID TEXT, Name TEXT, TimeStart BLOB, TimeStop BLOB)")
	cur.execute("INSERT INTO USED VALUES(?,?,?,?)", test)

con.commit() # commit values to makerspace database
con.close() # close makerspace database
