# ----------------------------------------------------------------------
# Numenta Platform for Intelligent Computing (NuPIC)
# Copyright (C) 2013, Numenta, Inc.  Unless you have an agreement
# with Numenta, Inc., for a separate license for this software code, the
# following terms and conditions apply:
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses.
#
# http://numenta.org/licenses/
# ----------------------------------------------------------------------
"""
Based on the hot gym tutorial
"""
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
  
def modelParamsToString(modelParams):
  pp = pprint.PrettyPrinter(indent=2)
  return pp.pformat(modelParams)

def writeModelParamsToFile(modelParams, name):
 
  with open(name, "wb") as outFile:
    modelParamsString = modelParamsToString(modelParams)
    if DEBUG:
      outFile.write(b'test')
    else:
      outFile.write("MODEL_PARAMS = \\\n".format(modelParamsString))


def run_swarms():
  '''Runs every swarm found in the directory structure found above using a local, scratch
        get the data directories, screen out git and other junk files'''
  dirs=[]
  for ddir in os.listdir(BASE_DIR):
    if os.path.isdir(os.path.join(BASE_DIR, ddir)) and ddir[0].isdigit(): 
      dirs.append(ddir)
      
  #for each of the swarm description directories, dig out the description files ...    
  swarm_files=[]
  for d in dirs:
    data_id = d.split('_')[0]
    swarm_files=os.listdir(os.path.join(BASE_DIR, d, data_id+'_swarm'))
    
    #All files in this dir with the right tag (naming convention) are swarm descriptors
    for source_file in swarm_files:
      if SWARM_DESC_TAG in source_file:
        #set up the scratch dir
        swarm_dir=tempfile.mkdtemp()
        sys.path.append(swarm_dir)
        
        #... make a scratch copy of the file and import the description dict
        swarm_file_name=os.path.join(swarm_dir, SWARM_DESC_TAG)
        shutil.copyfile(os.path.join(BASE_DIR, d, ODIR_SUBDIR.format(data_id), source_file), swarm_file_name )
        
        ##os.chdir(scatch)  not thread safe
        from swarm_description import SWARM_DESCTIPTION  
    
        #...and run the built in runWithConfig() method from permutaions_runner
        name = source_file.split('_swarm')[0]  #this will be something like '666_energy_only'
        param_fn = PARAMS_FILE.format(name) 
        print('running swarm for {} started {}'.
                      format(source_file.split('_swarm')[0],
                      datetime.now().strftime('%m-%d-%y  %H:%M')),
             end='' )
        
        if DEBUG:
          model_params = 'test params'
          with open(os.path.join(swarm_dir,  param_fn), 'w') as f:
            f.write (model_params)
          
        else:
          model_params = permutations_runner.runWithConfig(
            SWARM_DESCTIPTION,
            {"maxWorkers": MAX_WORKERS, "overwrite": True},
            outputLabel=name,
            outDir=swarm_dir,
            permWorkDir=swarm_dir,
            verbosity=0
          )    
        
        print('  ... finished at {}'.format(datetime.now().strftime('%m-%d-%y  %H:%M')))
              
        #dump parameters to the local scratch dir
       
        writeModelParamsToFile(model_params, param_fn)
        
        #finally, copy it back to the original data file directory
        shutil.copyfile(os.path.join(swarm_dir, param_fn), 
                        os.path.join(BASE_DIR, d, ODIR_SUBDIR.format(data_id), PARAMS_FILE.format(name))
                      )
        shutil.rmtree(swarm_dir)
  
if __name__ == "__main__":
  run_swarms()
