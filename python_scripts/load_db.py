'''Load a pecan street energy data from .csv file into a database'''
import mysql.connector
import sys

from database import login_info

FILE='d:\\pecan\\pecan_energy_hours'
DB = 'pecan'
TBL = 'demand'
KILL_TBL=True
TBL_CREATE='CREATE TABLE {}(dataid INT, tyme DATETIME, tz INT, euse FLOAT)'
TBL_INSERT='INSERT INTO {} (dataid, tyme, tz, euse) VALUES({}, {}, {}, {})'
NULL="NULL"

db=mysql.connector.Connect(**login_info)
curs = db.cursor()

if KILL_TBL:
	answer = input('gonna kill table ' + TBL + ', OK? (y/n) ')
	if answer == 'y':
		curs.execute('DROP TABLE IF EXISTS %s' %TBL)
		curs.execute(TBL_CREATE.format(TBL))
	else:
		print('Terminating')
		sys.exit()
		
with open(FILE, 'r') as f:
	#file header, data look like this:
	#    "dataid","localhour","use"
	#    22,"2013-06-22 19:00:00-05",0.75
	
	count = 0    #we'll commit every so many lines in case it crashes
	f.readline() #header
	for line in f:
		count += 1
		dataid, raw_time, euse = line.strip().split(',')
		tyme = '"' + raw_time[1:-4] + '"' #time stamp bit
		tz=raw_time[-3:-1]                #time zone at end
	
		try:	
			#TBL_INSERT='INSERT INTO {} (dataid, tyme, tz, euse) VALUES({}, {}, {}, {})'
			#dataid, type, tz, euse		
			TBL_INSERT.format(TBL, dataid, tyme, tz, euse)
			if not euse:
				euse=NULL
			curs.execute(TBL_INSERT.format(TBL, dataid, tyme, tz, euse))
				
		except:
			print('issue importing {}'.format(line))
		
		if not count%10000:
			print('committing at line {}'.format(count))
			db.commit()
		
	db.commit()
		
		

