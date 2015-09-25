"""
swarmFactory.py

Creates necessary file system objects objects to parametrize swarms based on different
configurations of input fields.  The idea is that each house has its own directory with
all necessary data, swarm configuration files, and run configuration files.  That way, 
the workload can be distributed across several virtuals - each working on its atomistic, 
parallel setup.

"""
#create csv file of relevant data for each house studied
#run a NuPIC swarm on each, storing the model parameters
#   - needs to be able to switch on weather, metorological, data
#   - needs to filter dates; maybe create a working data set in
#     the working directory
#
#these need to go in coded directory structures like
#d://pecan//house_data//6941_data/6941_input_data_csv


import  os
import csv
from pprint import pprint

from database import login_info
import testing_framework  #contains house id numbers

def csv_writer(o_file):
	return csv.writer(o_file, quoting=csv.QUOTE_NONE).writerow	

def csv_reader(i_file):
	return csv.reader(i_file)

def path_join(*args):
	"replaces os.path.join() for export to external virtual machines"
	my_path=''
	for ix, a in enumerate(args, start=1):
		my_path += str(a) 
		if ix < len(args):
			my_path += SEP
	return(my_path)

#file/directory names. For house 666, it looks like this:
#BASE_DIR
# --- 666_data
# --------666_input_data.csv
# --------666_clean_data.csv
# --- 666_swarm
# --------666_energy_only_swarm_description.py
# --------666_weather_swarm_description.py
# --------666_weather_plus_swarm_description.py

#update this as needed
BASE_DIR =         'd://pecan//house_data'
SEP =             '//'                         #path separator for workhorse machine

#but leave these alone, please
IDIR_SUBDIR =     '{}_data'
IFILE_NAME =      '{}_input_data.csv'          #house id as format() arg
CLEAN_DATA_NAME=  '{}_clean_data.csv'
ODIR_SUBDIR =     '{}_swarm'
OFILE_NAME =      '{}_{}_swarm_description.py' #house id, mode name as args


HOUSES =        testing_framework.training  #house id numbers

#the <house_id>_input data will be screened for this date range and show up in <house_id>_clean_data
FIRST_DATE =    '2013-03-10' #t[:10]  
LAST_DATE =     '2015-03-18'

#Field descriptor for available data, min/max values (rounded) taken over entire dataset
timestamp=      {'fieldName':'timestamp', 'fieldType':'datetime'}
euse=           {'fieldName':'euse',           'fieldType':'float', 'minvalue':10.0, 'maxvalue':35.0}
temp=           {'fieldName':'temp',           'fieldType':'float', 'minvalue':0.0,  'maxvalue':110.0}
humid=          {'fieldName':'humid',          'fieldType':'float', 'minvalue':0.0,  'maxvalue':100.0}
wind=           {'fieldName':'wind',           'fieldType':'float', 'minvalue':0.0,  'maxvalue':50.0}
cloud_cvr=      {'fieldName':'cloud_cvr',      'fieldType':'float', 'minvalue':0.0,  'maxvalue':0.0}
buildup=        {'fieldName':'buildup',        'fieldType':'float', 'minvalue':0.0,  'maxvalue':0.0}
is_daylight=    {'fieldName':'is_daylight',    'fieldType':'float', 'minvalue':0.0,  'maxvalue':0.0}
sec_since_rise= {'fieldName':'sec_since_rise', 'fieldType':'float', 'minvalue':10.0, 'maxvalue':50000}  

#set up different modes to include different fields  
modes={'energy_only' : [timestamp, euse],
       'weather'     : [timestamp, euse, temp, humid, wind],
       'weather_plus': [timestamp, euse, temp, humid, wind, 
                        is_daylight, buildup, sec_since_rise]
       }
#... keeping the column names in synch
##TODO:  gotta be a better way - this is redundent and repetitous.
column_names={'energy_only' : ['timestamp', 'euse'],
              'weather'     : ['timestamp', 'euse', 'temp', 'humid', 'wind'],
              'weather_plus': ['timestamp', 'euse', 'temp', 'humid', 'wind', 
                               'is_daylight', 'buildup', 'sec_since_rise']
       }

#the remaining swarm specification fields
PRED_FIELD = 'euse'
INFERENCE_TYPE= 'TemporalMultiStep'
STEPS      = 4
SWARM_SIZE = 'small'   #'medium' or 'large' for production

#rebuild the clean data sets
REBUILD_CLEAN_DATA =True

def write_swarm_description():
	#main loop for the different modes (fields included)
	for mode_name, fields in modes.items():
	
		#main loop to create the data files, one for each house
		for house in HOUSES:
			
			#set up the swarm directory, if necessary
			swarm_dir= path_join(BASE_DIR, IDIR_SUBDIR.format(house))
			if not os.path.exists(swarm_dir):
					os.mkdir(swarm_dir)	
			swarm_file_name = OFILE_NAME.format(house, mode_name)
			
			#input file (raw)
			raw_data_file = BASE_DIR + SEP + IDIR_SUBDIR.format(house) + SEP + IFILE_NAME.format(house) 
			
			#clean output data for swarm to work on - fully specified here:
			clean_data_file=path_join(BASE_DIR, IDIR_SUBDIR.format(house) ,CLEAN_DATA_NAME.format(house))
			#relative path here (assuming swarm will be run from swarm directory):
			clean_data_file_relative= path_join('..', CLEAN_DATA_NAME.format(house))
			
			#make sure we've got some raw data to work with
			if not os.path.exists(raw_data_file):
				raise FileNotFoundError("Sorry, can't find data for house{}".format(house))
			
			#create the descrition file based on the house id, fields, and other setup stuff
			SWARM_DESCRIPTION = {"includedFields": fields,
				                 "streamDef": {'info': 'kwh',
				                               'streams': [{'source': clean_data_file, 
			                                                'columns' : column_names[mode_name]} 
				                                           ] 
				                               },
				                 "inferenceType": INFERENCE_TYPE,
				                 "inferenceArgs": { "predictionSteps": [STEPS],
				                                    "predictionField": PRED_FIELD
				                                    },
	
				                 "iterationCount": -1,
				                 "swarmSize": SWARM_SIZE
				                 }
				
			#write the file - just a matter of dumping the swarm description
			print('this file has source data:', clean_data_file)	
			fn = path_join(BASE_DIR, IDIR_SUBDIR.format(house), ODIR_SUBDIR.format(house), swarm_file_name)
			with open(fn, 'w', newline='') as ofile:	                  
				ofile.write("'''Automatically generated swarm descrition file from swarm_factory.py'''")
				ofile.write("'''for house id #{}''' \n\n".format(house))
				ofile.write('SWARM_DESCTIPTION = ')
				pprint(SWARM_DESCRIPTION, stream=ofile)
				
			#Now, capture only the data between the FIRST_DATE and LAST_DATE, saving it to the swarm dir.
			#  (The raw data file contains *all* avaialable rows from the database.)
			
			if REBUILD_CLEAN_DATA:	
				started = False
				with open(raw_data_file, 'r') as ifile:
					reader=csv_reader(ifile)
					with open(clean_data_file, 'w') as ofile:
						writer=csv_writer(ofile)
						for row in reader:
							day=row[0][:10]  #yyyy-mm-dd bit of the datestamp
							if not started and day==FIRST_DATE:
								started=True
							if started:
								writer(row)
							if day == LAST_DATE:
								break
					
				


write_swarm_description()
a=1