#!/usr/bin/env python
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
Groups together code used for creating a NuPIC model and dealing with IO.
(This is a component of the One Hot Gym Prediction Tutorial.)
"""
import importlib
import sys
import csv
import datetime
import shutil
import os

from nupic.data.inference_shifter import InferenceShifter
from nupic.frameworks.opf.metrics import MetricSpec
from nupic.frameworks.opf.modelfactory import ModelFactory
from nupic.frameworks.opf.predictionmetricsmanager import MetricsManager

import nupic_output


DESCRIPTION = (
  "Starts a NuPIC model from the model params returned by the swarm\n"
  "and pushes each line of input from the gym into the model. Results\n"
  "are written to an output file (default) or plotted dynamically if\n"
  "the --plot option is specified.\n"
  "NOTE: You must run ./swarm.py before this, because model parameters\n"
  "are required to run NuPIC.\n"
)
GYM_NAME='sd_weather'
data_out=open('data_out.csv', 'w')
DATA_DIR = "."
MODEL_PARAMS_DIR = "./model_params"

DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

_METRIC_SPECS = (
    MetricSpec(field='kwh', metric='multiStep',
               inferenceElement='multiStepBestPredictions',
               params={'errorMetric': 'aae', 'window': 120,'steps': 1}),
    MetricSpec(field='kwh', metric='trivial',
               inferenceElement='prediction',
               params={'errorMetric': 'aae', 'window': 120,'steps': 1}),
    MetricSpec(field='kwh', metric='multiStep',
               inferenceElement='multiStepBestPredictions',
               params={'errorMetric': 'altMAPE', 'window': 120,'steps': 1}),
    MetricSpec(field='kwh', metric='multiStep',
               inferenceElement='multiStepBestPredictions',
               params={'errorMetric': 'altMAPE', 'window': 120,'steps': 4}),    
    MetricSpec(field='kwh', metric='trivial',
               inferenceElement='prediction',
               params={'errorMetric': 'altMAPE', 'window': 120,'steps': 1}),
)

def createModel(modelParams):
  import logging
  #model = ModelFactory.create(modelParams)
  model = ModelFactory.create(modelParams, logLevel=logging.DEBUG)
  model.enableInference({"predictedField": "kwh"})
  return model

def getModelParamsFromName(gymName):
  importName = "model_params.%s_model_params" % (
    gymName.replace(" ", "_").replace("-", "_")
  )
  print "Importing model params from %s" % importName
  try:
    importedModelParams = importlib.import_module(importName).MODEL_PARAMS
  except ImportError:
    raise Exception("No model params exist for '%s'. Run swarm first!"
                    % gymName)
  return importedModelParams



def runIoThroughNupic(inputData, model, gymName, plot):
  inputFile = open(inputData, "rb")
  #csvReader = csv.reader(inputFile)
  csvReader = csv.reader(inputFile)
  # skip header rows
  csvReader.next()
  csvReader.next()
  csvReader.next()

  shifter = InferenceShifter()
  if plot:
    output = nupic_output.NuPICPlotOutput([gymName])
  else:
    output = nupic_output.NuPICFileOutput([gymName])

  metricsManager = MetricsManager(_METRIC_SPECS, model.getFieldInfo(),
                                  model.getInferenceType())

  counter = 0

  #not quite sure best way to handle missing data, but for now use
  #last good value
  for row in csvReader:
    counter += 1
    timestamp = datetime.datetime.strptime(row[0], DATE_FORMAT)
    try:
       temp =  float(row[1])
    except:
       temp = temp
    try:
       dewpt = float(row[2])
    except:
       dewpt=dewpt
    try:
        wind =  float(row[3])
    except:
        wind=wind
    is_daylight = int(row[4])
    elapsed = int(row[5])
    kwh = float(row[6])
    
    result = model.run({
      "timestamp": timestamp,
      "temp":temp,
      "dewpt":dewpt,
      "wind": wind,
      "is_daylight":is_daylight,
      "elapsed":elapsed,
      "kwh":kwh,
      
    })
    result.metrics = metricsManager.update(result)

    if counter % 100 == 0:
      #print "Read %i lines..." % counter
      print "After %i records, 1-step aae=%f" \
            %(counter, 
              result.metrics["multiStepBestPredictions:multiStep:"
                            "errorMetric='altMAPE':steps=1:window=120:"
                            "field=kwh"]  
              )
      
      #print ("After %i records, 1-step aae=%f", 
             #counter,
              #result.metrics["multiStepBestPredictions:multiStep:"
                             #"errorMetric='aae':steps=1:window=120:"
                             #"field=kwh"])
 
    if plot:
      result = shifter.shift(result)

    prediction = result.inferences["multiStepBestPredictions"][1]
    output.write([timestamp], [kwh], [prediction])
    n=datetime.datetime.now()
    nstr=datetime.datetime.strftime(n,"%c")    
    data_out.write(nstr + ','  +  \
                   str(result.metrics["multiStepBestPredictions:multiStep:"
                                      "errorMetric='aae':steps=1:window=120:"
                                      "field=kwh"]) \
                   + ',' + \
                   str(result.metrics["multiStepBestPredictions:multiStep:"
                                      "errorMetric='altMAPE':steps=1:window=120:"
                                      "field=kwh"]) \
                   + ',' + \
                   str(result.metrics["multiStepBestPredictions:multiStep:"
                                      "errorMetric='altMAPE':steps=4:window=120:"
                                      "field=kwh"]) \
                                      
                   + ',' + \
                   datetime.datetime.strftime(timestamp, '%c')\
                   +'\n')
  inputFile.close()
  output.close()



def runModel(gymName, plot=False):
  inputData = "%s/%s.csv" % (DATA_DIR, gymName.replace(" ", "_"))
  pickleDir=os.path.join(os.getcwd(), 'pickle')
  iteration = 0
  while iteration < 101:
    print '*** iteration %i ***' %iteration
    if iteration == 0:
      print "Creating model from %s..." % gymName
      model = createModel(getModelParamsFromName(gymName))
    else:
      print "Reloading model - iteration %i" % iteration
      #we probably don't need to pickle the model here
      
      if os.path.exists(pickleDir):
        shutil.rmtree(pickleDir)      
      model.save(pickleDir)
      model = model.load(pickleDir)      
    
    runIoThroughNupic(inputData, model, gymName, plot)
    iteration +=1



if __name__ == "__main__":
  print DESCRIPTION
  plot = False
  args = sys.argv[1:]
  if "--plot" in args:
    plot = True
  runModel(GYM_NAME, plot=plot)
  data_out.close()
