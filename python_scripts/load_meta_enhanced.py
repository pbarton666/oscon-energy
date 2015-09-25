'''Load a pecan street metadata from .csv file'''
from database import login_info
import mysql.connector

FILE='d:\\pecan\\pecan_meta_enhanced.csv'
DB = 'pecan'
TBL = 'metaE'
KILL_TBL=True

#header, data look like this:
#"dataid","active_record","building_type","city","state","date_enrolled","date_withdrawn"
#2836,"","Single-Family Home","Austin","Texas","2011-02-01","2011-03-19"
#2743,"","Single-Family Home","Austin","Texas","2011-02-01","2011-09-01"

TBL_CREATE='''CREATE TABLE {}(
                              dataid INT, active VARCHAR(30), btype VARCHAR(50),
                              city VARCHAR(30), state VARCHAR(20), 
                              enrolled DATETIME, withdrawn DATETIME
                              )'''
TBL_INSERT='''INSERT INTO {} (dataid, active, btype, city, state, enrolled, withdrawn) 
               VALUES({}, {}, {}, {}, {}, {}, {})'''

db=mysql.connector.Connect(**login_info)
curs = db.cursor()

if KILL_TBL:
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
		dataid, active, btype, city, state, enrolled, withdrawn = line.strip().split(',')	
		if not active:
			active='NULL'
		if not btype:
			btype='NULL'		
		if enrolled=='""':
			enrolled='NULL'	
		if withdrawn=='""':
			withdrawn='NULL'			
		
		#print(TBL_INSERT.format(TBL, dataid, active, btype, city, state, enrolled, withdrawn))
		try:		
			curs.execute(TBL_INSERT.format(TBL, dataid, active, btype, city, state, enrolled, withdrawn))
		except:
			print('issue importing {}'.format(line))
		
		if not count%1000:
			print('committing at line {}'.format(count))
			db.commit()
	db.commit()	
		
		
		

