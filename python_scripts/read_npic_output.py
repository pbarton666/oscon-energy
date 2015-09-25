'''create a csv file for import to Excel containing data from
   100 runs of NuPIC against a single house in San Diego'''
"""
This script takes csv file of several runs of a nupic model run on a single data set
and creates another csv representation of them for creating comparisoins across runs.

The original data has one line per time step, reporting the timestamp, actual and predicted
values.  The new file rows are reported as:

timestamp, actual_value, predicted_value[run_1], predicted_value[run_2], ...

... which makes it easy to import into a spreadsheet to visualize learning as one run's
parameters are pickled then imported as a starting point for the next run.

The hard-coded file specs are for a single house in San Diego, with just over a year's worth
of hourly electric demand.
"""

import os
import csv
from collections import OrderedDict
import logging

DATADIR="D:\\pecan\\"
IN_FN= "sd_weather_out_21Jun.csv"
O_FN="sd_weather_out_parsed.csv"
SENTINAL = 'timestamp'
LOG_FILENAME = 'parse.log'
LOG_LEVEL = logging.DEBUG

logging.basicConfig(filename=LOG_FILENAME, level=LOG_LEVEL, new=True)
os.chdir(DATADIR)

def csv_writer(o_file):
    return csv.writer(o_file, quoting=csv.QUOTE_ALL).writerow

def csv_reader(i_file):
    return csv.reader(i_file)

this_pass= -1
ddict=OrderedDict()

i_file=open(DATADIR+IN_FN, 'r') 
data = i_file.readlines()
last=''
rnum=0

for row in data:
    rnum+=1
    #This traps and logs malformed output data.  Be sure the check the
    #  log file to insure any issue is not material
    try:
        ts, actual, predicted = row.split(',')
    except:
        logging.debug('had problems with {} at line {}, run ().'
                      'Substituted new run field'.
                      format(row, rnum, this_pass))
        row = 'timestamp,kw_energy_consumption,prediction\n'
        ts, actual, predicted = row.split(',')
     
   #store the data in a dict:
   #{timestamp, actual, prediction_run1, prediction_run2 ...}
     
    #Does this row begin a new run of the model, if so skip the sentinal line    
    if SENTINAL in ts:
        this_pass+=1
    
    #if this is the first pass, grab the actual and predicted value for this hour
    else:
        if not this_pass:  #first data block            
            ddict[ts] = [actual.strip(), predicted.strip()]
            
        #...otherwise just add the predicted value
        else:
            if ts in ddict:
                ddict[ts].extend([predicted.strip()])
    last=ts
                
with open(DATADIR+O_FN, 'w') as o_file:        
    writer=csv_writer(o_file)
    for k, v in ddict.items():
        writer([k] + v)
        
print("Finished!")        