from pprint import pprint as pp
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#from __future__ import print_function

import difflib
import datetime
from sys import version
import types
#basestring doesn't exist in python3.  Here's a patch from
# https://github.com/oxplot/fysom/issues/1
try:
    unicode = unicode
except NameError:
    # 'unicode' is undefined, must be Python 3
    str = str
    unicode = str
    bytes = bytes
    basestring = (str,bytes)
else:
    # 'unicode' exists, must be Python 2
    str = str
    unicode = unicode
    bytes = str
    basestring = basestring

try:
	from builtins import int
	#from past.builtins import basestring
	iteritems = dict.items
	##from six import iteritems
	six_builtins = True
	numbers = (int, float, complex, datetime.datetime)
except:
	print ("Please make sure you have 'future' and 'six' python packages installed.")

from collections import Iterable


class DeepDiff(object):

    def __init__(self, t1, t2):

        self.changes = {"type_changes": [], "dic_item_added": [], "dic_item_removed": [],
                        "values_changed": [], "unprocessed": [], "list_added": [], "list_removed": []}

        self.diffit(t1, t2)

        if six_builtins:
            self.changes = dict((k, v) for k, v in iteritems(self.changes) if v)
        else:
            self.changes = dict((k, v) for k, v in self.changes.iteritems() if v)

    def diffdict(self, t1, t2, parent):

        t2_keys, t1_keys = [
            set(d.keys()) for d in (t2, t1)
        ]

        t_keys_intersect = t2_keys.intersection(t1_keys)

        t_keys_added = t2_keys - t_keys_intersect
        t_keys_removed = t1_keys - t_keys_intersect

        if t_keys_added:
            self.changes["dic_item_added"].append("%s%s" % (parent, list(t_keys_added)))

        if t_keys_removed:
            self.changes["dic_item_removed"].append("%s%s" % (parent, list(t_keys_removed)))

        for item in t_keys_intersect:
            if isinstance(item, basestring):
                item_str = "'%s'" % item
            else:
                item_str = item
            self.diffit(t1[item], t2[item], parent="%s[%s]" % (parent, item_str))

    def diffit(self, t1, t2, parent="root"):

        if type(t1) != type(t2):
            self.changes["type_changes"].append("%s: %s=%s ===> %s=%s" % (parent, t1, type(t1), t2, type(t2)))

        elif isinstance(t1, basestring):
            diff = difflib.unified_diff(t1.splitlines(), t2.splitlines(), lineterm='')
            diff = list(diff)
            if diff:
                diff = '\n'.join(diff)
                self.changes["values_changed"].append("%s:\n%s" % (parent, diff))

        elif isinstance(t1, numbers):
            if t1 != t2:
                self.changes["values_changed"].append("%s: %s ===> %s" % (parent, t1, t2))

        elif isinstance(t1, dict):
            self.diffdict(t1, t2, parent)

        elif isinstance(t1, Iterable):

            try:
                t1_set = set(t1)
                t2_set = set(t2)
            # When we can't make a set since the iterable has unhashable items
            except TypeError:

                for i, (x, y) in enumerate(zip(t1, t2)):

                    self.diffit(x, y, "%s[%s]" % (parent, i))

                if len(t1) != len(t2):
                    items_added = [item for item in t2 if item not in t1]
                    items_removed = [item for item in t1 if item not in t2]
                else:
                    items_added = None
                    items_removed = None
            else:
                items_added = list(t2_set - t1_set)
                items_removed = list(t1_set - t2_set)

            if items_added:
                self.changes["list_added"].append("%s: %s" % (parent, items_added))

            if items_removed:
                self.changes["list_removed"].append("%s: %s" % (parent, items_removed))

        else:
            try:
                t1_dict = t1.__dict__
                t2_dict = t2.__dict__
            except AttributeError:
                pass
            else:
                self.diffdict(t1_dict, t2_dict, parent)

        return



class DictDiffer(object):
    """
	http://stackoverflow.com/questions/1165352/fast-comparison-between-two-python-dictionary
    Calculate the difference between two dictionaries as:
    (1) items added
    (2) items removed
    (3) keys same in both but changed values
    (4) keys same in both and unchanged values
    """
    def __init__(self, current_dict, past_dict):
        self.current_dict, self.past_dict = current_dict, past_dict
        self.set_current, self.set_past = set(current_dict.keys()), set(past_dict.keys())
        self.intersect = self.set_current.intersection(self.set_past)
    def added(self):
        return self.set_current - self.intersect 
    def removed(self):
        return self.set_past - self.intersect 
    def changed(self):
        return set(o for o in self.intersect if self.past_dict[o] != self.current_dict[o])
    def unchanged(self):
        return set(o for o in self.intersect if self.past_dict[o] == self.current_dict[o])

MODEL_PARAMS_GYM = \
{ 'aggregationInfo': { 'days': 0,
                       'fields': [],
                       'hours': 0,
                       'microseconds': 0,
                       'milliseconds': 0,
                       'minutes': 0,
                       'months': 0,
                       'seconds': 0,
                       'weeks': 0,
                       'years': 0},
  'model': 'CLA',
  'modelParams': { 'anomalyParams': { u'anomalyCacheRecords': None,
                                      u'autoDetectThreshold': None,
                                      u'autoDetectWaitRecords': None},
                   'clParams': { 'alpha': 0.030563523414682152,
                                 'clVerbosity': 0,
                                 'regionName': 'CLAClassifierRegion',
                                 'steps': '1'},
                   'inferenceType': 'TemporalMultiStep',
                   'sensorParams': { 'encoders': { '_classifierInput': { 'classifierOnly': True,
                                                                         'clipInput': True,
                                                                         'fieldname': 'kw_energy_consumption',
                                                                         'maxval': 53.0,
                                                                         'minval': 0.0,
                                                                         'n': 175,
                                                                         'name': '_classifierInput',
                                                                         'type': 'ScalarEncoder',
                                                                         'w': 21},
                                                   u'kw_energy_consumption': { 'clipInput': True,
                                                                               'fieldname': 'kw_energy_consumption',
                                                                               'maxval': 53.0,
                                                                               'minval': 0.0,
                                                                               'n': 25,
                                                                               'name': 'kw_energy_consumption',
                                                                               'type': 'ScalarEncoder',
                                                                               'w': 21},
                                                   u'timestamp_dayOfWeek': None,
                                                   u'timestamp_timeOfDay': { 'fieldname': 'timestamp',
                                                                             'name': 'timestamp',
                                                                             'timeOfDay': ( 21,
                                                                                            5.237075943768415),
                                                                             'type': 'DateEncoder'},
                                                   u'timestamp_weekend': { 'fieldname': 'timestamp',
                                                                           'name': 'timestamp',
                                                                           'type': 'DateEncoder',
                                                                           'weekend': ( 21,
                                                                                        1)}},
                                     'sensorAutoReset': None,
                                     'verbosity': 0},
                   'spEnable': True,
                   'spParams': { 'columnCount': 2048,
                                 'globalInhibition': 1,
                                 'inputWidth': 0,
                                 'maxBoost': 2.0,
                                 'numActiveColumnsPerInhArea': 40,
                                 'potentialPct': 0.8,
                                 'seed': 1956,
                                 'spVerbosity': 0,
                                 'spatialImp': 'cpp',
                                 'synPermActiveInc': 0.05,
                                 'synPermConnected': 0.1,
                                 'synPermInactiveDec': 0.057337836954690545},
                   'tpEnable': True,
                   'tpParams': { 'activationThreshold': 14,
                                 'cellsPerColumn': 32,
                                 'columnCount': 2048,
                                 'globalDecay': 0.0,
                                 'initialPerm': 0.21,
                                 'inputWidth': 2048,
                                 'maxAge': 0,
                                 'maxSegmentsPerCell': 128,
                                 'maxSynapsesPerSegment': 32,
                                 'minThreshold': 10,
                                 'newSynapseCount': 20,
                                 'outputType': 'normal',
                                 'pamLength': 3,
                                 'permanenceDec': 0.1,
                                 'permanenceInc': 0.1,
                                 'seed': 1960,
                                 'temporalImp': 'cpp',
                                 'verbosity': 0},
                   'trainSPNetOnlyIfRequested': False},
  'predictAheadTime': None,
  'version': 1}

MODEL_PARAMS_SD = \
{ 'aggregationInfo': { 'days': 0,
                       'fields': [],
                       'hours': 0,
                       'microseconds': 0,
                       'milliseconds': 0,
                       'minutes': 0,
                       'months': 0,
                       'seconds': 0,
                       'weeks': 0,
                       'years': 0},
  'model': 'CLA',
  'modelParams': { 'anomalyParams': { u'anomalyCacheRecords': None,
                                      u'autoDetectThreshold': None,
                                      u'autoDetectWaitRecords': None},
                   'clParams': { 'alpha': 0.020528037320708514,
                                 'clVerbosity': 0,
                                 'regionName': 'CLAClassifierRegion',
                                 'steps': '1'},
                   'inferenceType': 'TemporalMultiStep',
                   'sensorParams': { 'encoders': { '_classifierInput': { 'classifierOnly': True,
                                                                         'clipInput': True,
                                                                         'fieldname': 'kwh',
                                                                         'maxval': 5.18,
                                                                         'minval': 0.0,
                                                                         'n': 131,
                                                                         'name': '_classifierInput',
                                                                         'type': 'ScalarEncoder',
                                                                         'w': 21},
                                                   u'dewpt': None,
                                                   u'elapsed': None,
                                                   u'is_daylight': None,
                                                   u'kwh': { 'clipInput': True,
                                                             'fieldname': 'kwh',
                                                             'maxval': 5.18,
                                                             'minval': 0.0,
                                                             'n': 130,
                                                             'name': 'kwh',
                                                             'type': 'ScalarEncoder',
                                                             'w': 21},
                                                   u'temp': None,
                                                   u'timestamp_dayOfWeek': None,
                                                   u'timestamp_timeOfDay': { 'fieldname': 'timestamp',
                                                                             'name': 'timestamp',
                                                                             'timeOfDay': ( 21,
                                                                                            2.3616750299601295),
                                                                             'type': 'DateEncoder'},
                                                   u'timestamp_weekend': None,
                                                   u'wind': None},
                                     'sensorAutoReset': None,
                                     'verbosity': 0},
                   'spEnable': True,
                   'spParams': { 'columnCount': 2048,
                                 'globalInhibition': 1,
                                 'inputWidth': 0,
                                 'maxBoost': 2.0,
                                 'numActiveColumnsPerInhArea': 40,
                                 'potentialPct': 0.8,
                                 'seed': 1956,
                                 'spVerbosity': 0,
                                 'spatialImp': 'cpp',
                                 'synPermActiveInc': 0.05,
                                 'synPermConnected': 0.1,
                                 'synPermInactiveDec': 0.1},
                   'tpEnable': True,
                   'tpParams': { 'activationThreshold': 13,
                                 'cellsPerColumn': 32,
                                 'columnCount': 2048,
                                 'globalDecay': 0.0,
                                 'initialPerm': 0.21,
                                 'inputWidth': 2048,
                                 'maxAge': 0,
                                 'maxSegmentsPerCell': 128,
                                 'maxSynapsesPerSegment': 32,
                                 'minThreshold': 10,
                                 'newSynapseCount': 20,
                                 'outputType': 'normal',
                                 'pamLength': 1,
                                 'permanenceDec': 0.1,
                                 'permanenceInc': 0.1,
                                 'seed': 1960,
                                 'temporalImp': 'cpp',
                                 'verbosity': 0},
                   'trainSPNetOnlyIfRequested': False},
  'predictAheadTime': None,
  'version': 1}

#pp(MODEL_PARAMS_GYM)
s=MODEL_PARAMS_SD
g=MODEL_PARAMS_GYM

d = DeepDiff(s, g)

pp(d.changes)