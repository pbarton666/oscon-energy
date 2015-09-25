
"""Calculate heat buildup values, defined here as the cumulative departure
   from a comfortable temperature over a the lst H hours.  Augment weather
   data with this value in a new, separate table in the same database."""

from database import login_info
import mysql.connector
from collections import deque

KILL_TBL = True
TBL = 'weather'      #original data table
NEW_TABLE = 'demandE'

TARGET = 72            #target temp in degrees F
WINDOW = 72            #heat buildup window
DUMMY_VAL = -666

def dbfix(val):
	"creates a quoted, value for insertion to db. Also creates 'NULL' for missing data"
	if not val: 
		return "NULL"
	else:
		return '"' + str(val) + '"'

def build_weights(old_weight=.5, mid_weight=1.0, recent_weight=2.0, window=WINDOW):
	'''Let's make up a rule that high temp in the middle of the window contributes to heat buildup,
	   high temp in the last third contributes twice that, and first third half that'''
	weights = [old_weight]*(window//3)
	weights.extend([mid_weight] * (window//3))
	weights.extend([recent_weight] * (window - len(weights)))	
	return weights

def update_buildup(deck, weights, temp, target=TARGET):
	'''deck is a double-ended queue of temp data, weights is weighting vector.
	   We'll use them to create a weighted heat buildup metric
	   SUM( weights[earliest...latest] * (deck[earliest...latest temps] - TARGET))
		  
	Note:  this is only useful after both are fully populated.'''
	
	try:
		deck.popleft()
	except IndexError:
		pass #nothing to pop
	if temp:
		deck.append(temp)
	else:
		deck.append(DUMMY_VAL)
	#gin up a weighted heat buildup based only on good temps
	buildup =0
	for w, d in zip (weights, deck):
		if d != DUMMY_VAL:
			buildup += w * (d - target)
			
	return (deck, buildup)

def create_weather_dict(window=WINDOW):
	'''Starting with baseline weather data, create a dict (key is a timestamp)
	   with key atmospheric data, supplemented by a heat buildup metric
	   
	   Note: this currently hard-wired for Austin weather from the Pecan St. database.'''
	
	#we'll use a queue for the temps and a list of equal length for the weights
	deck = deque(maxlen=window)
	weights=build_weights()
	
	#this gets the weather data for Meuller Airport in Austin, TX
	weather_sql = """SELECT tyme, temp, humid, wind, cloud_cvr 
		          FROM weather 
		          WHERE lat > 30 and lat < 31 and longi < -97 and longi > -98 
		          ORDER BY tyme"""
	tbl_insert= """INSERT INTO {} """	
	
	#now, we'll build our augmented weather dict
	db=mysql.connector.Connect(**login_info)
	curs = db.cursor()
	
	wdict={}
	buildup = 0
	
	curs.execute(weather_sql)
	for ix, line in enumerate(curs.fetchall()):
		tyme, temp, humid, wind, cloud_cvr = line
		#manage temp queue, return current heat buildup 'offline'
		deck, buildup = update_buildup(deck, weights, temp)
		#now we have a dict where we can pick off all the atmospherics by timestamp
		wdict[tyme] = {'temp':temp, 'humid':humid, 'wind':wind, 'cloud_cvr':cloud_cvr, 'buildup':buildup}	
		
	return wdict
		
def make_temp_table():
	"""Create a customized table, just for single family houses in Austin, still actively
	    providing meter data, augmented with weather data."""
	
	TBL_CREATE="""CREATE TABLE {}(dataid INT, tyme DATETIME, tz INT, 
	                              euse FLOAT, temp FLOAT, humid FLOAT, 
	                              wind FLOAT, cloud_cvr FLOAT, buildup FLOAT
	                              )
	                              """
	TBL_INSERT="""INSERT INTO {} (dataid, tyme, tz, 
	                              euse, temp, humid, 
	                              wind, cloud_cvr, buildup
	                              ) 
	                              VALUES({}, {}, {}, {}, {}, {}, {}, {}, {})"""	
	
	META_SELECT="""SELECT dataid 
	              FROM metaE 
	              WHERE 
	              city ='Austin' and 
	              btype like 'Single%' and 
	              active='yes' and 
	              year(enrolled)=2011"""
	
	ENERGY_SELECT="""SELECT dataid, tyme, tz, euse
	                 FROM demand
	                 WHERE dataid={}
	                 ORDER BY tyme 
	                 LIMIT 50000"""
	
	#db connection w/ a couple of cursors	
	db=mysql.connector.Connect(**login_info)
	curs = db.cursor()
	insert_curs =db.cursor()
	
	#build weighted tables to calculate heat buildup
	weights=build_weights()            #weights
	wdict=create_weather_dict(WINDOW)  #create a dict of the atmospheric data and heat buildup 
	
	#add a new table
	if KILL_TBL:
		#answer = 'y'
		answer = input('gonna kill table ' + NEW_TABLE + ', OK? (y/n) ')
		if answer == 'y':
			curs.execute('DROP TABLE IF EXISTS %s' %NEW_TABLE)
			curs.execute(TBL_CREATE.format(NEW_TABLE))
	
	#Grab the qualifying house from the enhanced metadata. (SF houses in Austin w/ lot of data)
	houseids=[]
	curs.execute(META_SELECT)	
	for row in curs.fetchall():
		houseids.append(row[0])
		
	#Get energy data for each house and combine it with atmospherics for new table	
	for houseid in houseids:
		if houseid not in [18 , 35, 114]:
			#pull the energy data for this house
			curs.execute(ENERGY_SELECT.format(houseid))
			print('looking at id:' ,houseid)
			for row in curs.fetchall():
					dataid, tyme, tz, euse=row
					try:
						wdata = wdict[tyme]   
					except KeyError:
						#print('sorry no weather data for', tyme)
						continue
					insert_curs.execute(TBL_INSERT.format(NEW_TABLE,
					                                      dbfix(houseid),
						                                  dbfix(tyme),
						                                  dbfix(tz),
						                                  dbfix(euse),
						                                  dbfix( wdata['temp']),
						                                  dbfix(wdata['humid']),
						                                  dbfix(wdata['wind']),
						                                  dbfix(wdata['cloud_cvr']),
						                                  dbfix(wdata['buildup'])
						                                  
						                                  )
						                )
		
					
					if euse:
						pass
						#print('inserted', houseid, tyme, tz, euse, wdata)
			db.commit()
			print('finished house:', houseid)
	
		
if __name__=='__main__':
	create_weather_dict()
	make_temp_table()

