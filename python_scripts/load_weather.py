'''Load a pecan street weather data from .csv file'''
from database import login_info
import mysql.connector

FILE='d:\\pecan\\pecan_weather.csv'
DB = 'pecan'
TBL = 'weather'
KILL_TBL=True

#header, data looks like this:
#"localhour","latitude","longitude","tz_offset","temperature","temperature_error","humidity","humidity_error","wind_speed","cloud_cover"
#"2012-06-10 09:00:00-05",30.292432,-97.699662,-5,77.68,,0.8,,9.19,0.85
#"2012-06-10 10:00:00-05",30.292432,-97.699662,-5,81.79,,0.69,,11.21,0.46

TBL_CREATE='''CREATE TABLE {}(tyme DATETIME,
                              lat FLOAT, 
                              longi FLOAT,
                              tz_offset INT(3),
                              temp FLOAT,
                              temp_err FLOAT,
                              humid FLOAT,
                              humid_err FLOAT,
                              wind FLOAT,
                              cloud_cvr FLOAT,
                              tz INT(3)
                              )'''
TBL_INSERT='''INSERT INTO {} (tyme, lat, longi, 
                              tz_offset, temp, temp_err, 
                              humid, humid_err, wind, 
                              cloud_cvr, tz
                              ) 
                              VALUES({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}
                              )'''

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
		raw_time, lat, longi, tz_offset, temp, temp_err, humid, humid_err, wind, cloud_cvr \
           = line.strip().split(',')
		
		#timestamp is ugly:  "2012-06-10 09:00:00-05"
		tyme = '"' + raw_time[1:-4] + '"' #time stamp bit
		tz=raw_time[-3:-1]                #time zone at end
		
		if not temp:
			temp='NULL'			
		if not temp_err:
			temp_err='NULL'
		if not humid:
			humid='NULL'				
		if not humid_err:
			humid_err='NULL'
		if not wind:
			wind='NULL'	
		if not cloud_cvr:
			cloud_cvr='NULL'				

		try:	
			curs.execute(TBL_INSERT.format(TBL, tyme, lat, longi, tz_offset, temp, temp_err, humid, humid_err, wind, cloud_cvr, tz))				
		except:
			print('issue importing {}'.format(line))		
		if not count%1000:
			print('committing at line {}'.format(count))
			db.commit()
	db.commit()
		
		
		
		

