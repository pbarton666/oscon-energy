'''Load a pecan street metadata from .csv file'''
from database import login_info
import mysql.connector

FILE='d:\\pecan\\pecan_meta.csv'
DB = 'pecan'
TBL = 'meta'
KILL_TBL=True

#header, data look like this:
#"dataid","city","state","pv"
#2836,"Austin","Texas",""
#2743,"Austin","Texas",""

TBL_CREATE='CREATE TABLE {}(dataid INT, city VARCHAR(30), state VARCHAR(20), pv VARCHAR(10))'
TBL_INSERT='INSERT INTO {} (dataid, city, state, pv) VALUES({}, {}, {}, {})'

db=mysql.connector.Connect(**login_info)
curs = db.cursor()

if KILL_TBL:
	x=1
	answer = input('gonna kill table ' + TBL + ', OK? (y/n) ')
	#answer='y'
	if answer == 'y':
		curs.execute('DROP TABLE IF EXISTS %s' %TBL)
		curs.execute(TBL_CREATE.format(TBL))
		
with open(FILE, 'r') as f:
	
	count = 0  #we'll commit every so many lines in case it crashes
	f.readline() #header
	for line in f:
		count += 1
		pv='NULL'
		dataid, city, state, pv = line.strip().split(',')	
		try:		
			curs.execute(TBL_INSERT.format(TBL, dataid, city, state, pv))
		except:
			print('issue importing {}'.format(line))
		
		if not count%1000:
			print('committing at line {}'.format(count))
			db.commit()
	db.commit()	
		
		
		

