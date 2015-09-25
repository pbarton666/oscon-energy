"""
build_nupic_run_data.py

Generates NuPIC friendly text files from data stored in MySQL db.

Stores them in directories code-named with house id numbers (in a
data subdir).
"""

##TODO: limit dates here or in swarm factory

#NuPIC file header:
#timestamp,temp,dewpt,wind,is_daylight,elapsed,kwh
#datetime, float, float, float, int, int, float
#T,,,,,,
#2011-02-01 01:00:00,16.1,9.4,2.6,0,0,0.385
#2011-02-01 02:00:00,15,10,1.5,0,0,0.365

#Data tables:
#demande:  dataid, tyme, tz, euse, temp, humid, wind, clout_cvr buildup
#sun:  time, is_daylight, rise, set, seconds_daylight, seconds_since_rise, city, state
#NB sun time is local standard time, demande tyme is local daylight time

import  datetime, sys, os, csv
from database import login_info
#import mysql.connector
#mysql.connector.errors.InterfaceError: 2013: Lost connection to MySQL server during query w/ mysql.connector.  
#Known bug.  http://stackoverflow.com/questions/26510114/why-does-mysql-connector-break-lost-connection-to-mysql-server-during-query-e
import pymysql

import testing_framework  #contains house id numbers

BASE_ODIR =    'd://pecan//house_data//'
ODIR_SUBDIR =  '{}_data'
OFILE_NAME =   '{}_input_data.csv'  #takes house id as format() arg
DB_NAME =      'pecan'
ASTRO_TABLE=   'sun'                #'sun_test'
ENERGY_TABLE=  'demande'            #'demande_test'
LIMIT=          1000000             #20000
HOUSES =        testing_framework.training  #house id numbers



#data processing SQL
SQL= """SELECT d.dataid, d.tyme, d.euse, d.temp, d.humid, d.wind, d.cloud_cvr, d.buildup,
        s.is_daylight, s.seconds_since_rise from {} d
        INNER JOIN {} s
        ON d.tyme = s.time
        WHERE d.dataid = {}
        limit {}
"""
def csv_writer(o_file):
    return csv.writer(o_file, quoting=csv.QUOTE_NONE).writerow

def process_missing(thing):
	"Handle missing data"
	if not thing:
		thing=''
	return thing
	
#set up the database
#db=mysql.connector.Connect(**login_info)
db=pymysql.connect(**login_info)
curs = db.cursor()
curs.execute("USE {}".format(DB_NAME))

#main loop to create the data files
for house in HOUSES:
	this_dir=os.path.join(BASE_ODIR, ODIR_SUBDIR.format(house))
	if not os.path.exists(this_dir):
			os.mkdir(this_dir)
	os.chdir(this_dir)
		
	with open(OFILE_NAME.format(house), 'w', newline='') as ofile:	                  
			writer=csv_writer(ofile)
			#headers
			writer(['timestamp', 'euse', 'temp', 'humid', 'wind', 'cloud_cvr', 'buildup', 'is_daylight', 'sec_since_rise']) 
			writer(['datetime', 'float', 'float', 'float', 'float', 'float', 'float', 'float', 'float'])
			writer(['T','','','','','','','',''])
						
			#pull data from this house from the DB, process it, and write it
			print("data pull for house {} ...".format(house), end='')
			query=SQL.format(ENERGY_TABLE, ASTRO_TABLE, house, LIMIT)
			curs.execute(query)
			print('  COMPLETE.')
						
			#format NuPIC-friendly text data
			row_num = 0
			while True:
				r=curs.fetchone()
				if r:
					dataid, tyme, euse, temp, humid, wind, cloud_cvr, buildup, is_daylight, sec_since_rise = r
					#convert to friendly format
					mytime= tyme.strftime('%Y-%m-%d %H:%M:%S')
					euse=process_missing(euse)
					temp=process_missing(temp)
					humid=process_missing(humid)
					wind=process_missing(wind)
					cloud_cvr=process_missing(cloud_cvr)
					buildup=process_missing(buildup)
					is_daylight=process_missing(is_daylight)
					sec_since_rise=process_missing(sec_since_rise)
					fields = [tyme, euse, temp, humid, wind, cloud_cvr, buildup, is_daylight, sec_since_rise]
					writer(fields)
					if row_num and not row_num % 1000:
						print('   processing row {}'.format(row_num))
					row_num+=1									
				else:
					break
			print('read {} rows'.format(row_num))


a=1


             
             
