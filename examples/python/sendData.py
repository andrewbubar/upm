#!/usr/bin/python

import sqlite3 as lite
import csv

# write to backup.csv file
with open('backup.csv', 'w+') as write_file:
	con = lite.connect('makerspace.db') # connect to database
	cur = con.cursor() # set cursor
	
	# retrieve values from table and write to file
	for row in cur.execute('SELECT * FROM USED'):
		write_file.write(','.join(row))
		write_file.write('\n')
    
