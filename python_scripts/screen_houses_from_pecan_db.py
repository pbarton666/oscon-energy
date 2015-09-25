"""This script selects individual houses from the pecan meta data table based on 
    elegibility criteria and stores them in a sample table.  The eligibility critera
    are embedded in the SQL statement at line 44.  Pretty one-off, needless to say.

	Then, for each of the houses, it queries the energy table for the first and 
	last dates of hourly energy consumption measurements
	"""
import mysql.connector
import csv

from database import login_info
from testing_framework import known_bad

DB = 'pecan'
UPDATE_ELIBIBILITY=True
O_FILE = 'data_grid.csv'

def csv_writer(o_file):
    return csv.writer(o_file, quoting=csv.QUOTE_NONNUMERIC).writerow

db=mysql.connector.Connect(**login_info)
curs = db.cursor()

curs.execute('use {}'.format(DB))

if UPDATE_ELIBIBILITY:
#creates a table of our elibible houses for future reference

#To create a display of the data and duration, we need the min and max dates from this selection.  The query
# takes forever to run, so the dates are hardwired below; update as necessary

    not_run_here="""select min(yearweek(tyme)), max(yearweek(tyme)), min(tyme), max(tyme)
                    from demande d,
				         metae m
	                where d.dataid = m.dataid"""	

    curs.execute('use {}'.format(DB))
    curs.execute('drop table if exists sample_ids')
    #Get single family houses only from Austin, that enrolled early and are still active
    #   Of course, this can be changed easily.
    curs.execute("""create table sample_ids 
		                  SELECT dataid  
		                  FROM metaE   
		                  WHERE city ='Austin' and   
                                btype like 'Single%' and  
                                active='yes' and   
                                year(enrolled)=2011 
		                  """)
    db.commit()

#first and last dates from not_run_here query	
global_first = 201201 #2012-01-01 00:00:00  
global_last = 201511  #2015-03-18 23:00:00



#sorted list of all eligible yrweeks
curs.execute("""select distinct yearweek(tyme)   from demande
                     where yearweek(tyme) >= 201201 and yearweek(tyme) <= 201511
	                 order by yearweek(tyme)""")
yrweeks =[]
for data in curs.fetchall():
    yrweeks.append(data[0])
db.commit()

#eligible houses
curs.execute("select * from sample_ids")
elig = []
for data in curs.fetchall():
    elig.append(data[0])
db.commit()

#Create a grid of houses * yrweeks in an Excel-importable file.  This will need
#  further screening to weed out those with spotty data, etc.  Currently done
#  manually.
with open(O_FILE, 'w') as ofile:
    writer=csv_writer(ofile)
    #write the yearweek header in the top 
    arr=['']
    arr.extend(yrweeks)
    writer(arr)            
    minyw, maxyw = catch[0]    

    #get first and last dates for each house
    for house in elig:
        if house in known_bad: #known bad data
            continue
        curs.execute("""select min(yearweek(tyme)), max(yearweek(tyme))
							from demande
							where dataid = {}
							""".format(house))
        catch=curs.fetchall()
        if not catch[0][0]:  #check for valid data return
            print('dumping house {} - no data; please add to known_bad'.format(house))
            continue
        else:

            #compose an array to write
            started = False
            arr = [house]
            #we'll put an 'x' or a null char in the row, depending of whether there's data
            for yw in yrweeks:
                if not started:
                    if yw == minyw:
                        started=True
                if started:
                    arr.append('x')
                else:
                    arr.append('')
                #if this is the last week, we're done with the house   
                if yw == maxyw: 
                    writer(arr)
                    break
    db.commit()

