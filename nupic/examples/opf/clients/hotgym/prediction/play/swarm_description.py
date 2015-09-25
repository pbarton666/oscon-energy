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

SWARM_DESCRIPTION = {
  "includedFields": [
    {
      "fieldName": "timestamp",
      "fieldType": "datetime"
    },
    {
      "fieldName":"temp",
      "fieldType":"float",
      "maxValue":34.0,
      "minValue":6.0
    },
    {
      "fieldName":"dewpt",
      "fieldType":"float",
      "maxValue":22.0,
      "minValue":-22.0
    },
    {
     "fieldName":"wind",
     "fieldType":"float",
     "maxValue": 14.0,
     "minValue": 0.0     
     },
     {
     "fieldName":"is_daylight",
     "fieldType":"int",
     "maxValue":1, 
     "minValue":0
      },
      {
      "fieldName":"elapsed",
      "fieldType":"int",
      "maxValue":86400,
      "minValue":0
       },
       {
      "fieldName":"kwh", 
      "fieldType":"float",
      "maxValue":5.18,
      "minValue":0.0
       },
    
  ],
  "streamDef": {
    "info": "kw_energy_consumption",
    "version": 1,
    "streams": [
      {
	"info": "San Diego",
        #"info": "Rec Center",
        #"source": "file://rec-center-hourly.csv",
        "source":"file://sd_weather.csv",
        "columns": [
          "*"
        ]
      }
    ]
  },
  #new added by pat
#  "metricWindow": 24,

  "inferenceType": "TemporalMultiStep",
  "inferenceArgs": {
    "predictionSteps": [
      1
    ],
    "predictedField": "kwh"
  },
  "iterationCount": -1,
  "swarmSize": "medium"
  #"swarmSize":"small"
}
