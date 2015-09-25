import os
import pprint
import tempfile
import shutil
from datetime import datetime
import sys

# add logging to output errors to stdout
import logging
logging.basicConfig()

#file/directory names. For house 666, it looks like this:
#BASE_DIR
# --- 666_data
# --------666_input_data.csv
# --------666_clean_data.csv
# ------- 666_swarm
# -------------666_energy_only_swarm_description.py
# -------------666_weather_swarm_description.py
# -------------666_weather_plus_swarm_description.py
#              (added here)
# -------------666_energy_only_model_params.py
# -------------666_weather_model_params.py
# -------------666_weather_plus_model_params.py

#update this as needed
##TODO: move to a config file

BASE_DIR =         'd://pecan//house_data//'
#but leave these alone, please
IDIR_SUBDIR =     '{}_data'
IFILE_NAME =      '{}_input_data.csv'          #house id as format() arg
CLEAN_DATA_NAME=  '{}_clean_data.csv'
ODIR_SUBDIR =     '{}_swarm'
SWARM_DESC_TAG =   'swarm_description.py'
OFILE_NAME =      '{}_{}_' + SWARM_DESC_TAG   #house id, mode name as args
PARAMS_DIR =      'model_params'
PARAMS_FILE =     '{}_model_params.py'

MAX_WORKERS =     4   #process treads

##TODO:  get rid of the debug
DEBUG = True  
if not DEBUG:
  from nupic.swarming import permutations_runner
  from swarm_description import SWARM_DESCRIPTION
  

def cleanup():
  '''one-off utility to clean directoris fould by debugging'''
  dirs=[]
  for ddir in os.listdir(BASE_DIR):
    if os.path.isdir(os.path.join(BASE_DIR, ddir)) and ddir[0].isdigit(): 
      dirs.append(ddir)
      
  #for each of the swarm description directories, dig out the description files ...    

  for d in dirs:
    thisdir = os.path.join(BASE_DIR, d)
    files= os.listdir(thisdir)
    for f in files:
      if f.endswith('.py'):
        fn = os.path.join(BASE_DIR, d, f)
        print('removing: ', fn)
        os.remove(fn)
                  
   
        
if __name__ == '__main__':
  cleanup()