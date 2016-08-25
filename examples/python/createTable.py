#!/usr/bin/python
import sqlite3 as lite

con = lite.connect('makerspace.db')

people = (
	("9621023222", 'Andrew Bubar', 'Y', 'Y', 'Y'),
        (2, 'Chris Ross', 'Y', 'Y', 'Y'),
        ("321143517", 'Hunter Pickett', 'N', 'N', 'N'),
        (4, 'Ashish Datta', 'Y','Y','Y')
        )

with con:
	cur = con.cursor()
	
	cur.execute("DROP TABLE IF EXISTS PERMISSIONS")
	cur.execute("CREATE TABLE PERMISSIONS(ID TEXT, Name TEXT, Laser TEXT, Printer TEXT, Solder TEXT)")
    	cur.executemany("INSERT INTO Permissions VALUES(?,?,?,?,?)",people)

con.commit()
con.close()
