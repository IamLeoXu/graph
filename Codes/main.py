from IPython.display import display      # Creates an audio object. Lets you play audio directly in an IPython notebook.
from IPython import get_ipython
import wfdb as wf
from wfdb import processing
import glob, os
import numpy as np
import pandas as pd
import biosppy
import subprocess
import pyhrv
import pyhrv.tools as tools
#from pyhrv import hrv_report
import pyhrv.time_domain as td
from pyhrv.hrv import hrv
from pyhrv.time_domain import nnXX
from pyhrv.time_domain import nn50
from pyhrv.time_domain import nn20
from biosppy import utils
from biosppy.signals import ecg
import shutil  # module offers a number of high-level operations on files and collections of files.
import PyQt6, PySide6, PyQt5, PySide2

# In particular, functions are provided which support file copying and removal.
# For operations on individual files, see also the os module.

import posixpath   # module provides os.path functionality on Unix and other POSIX-compatible platforms.

# The Portable Operating System Interface (POSIX) is a family of standards specified by
# the IEEE Computer Society for maintaining compatibility between operating systems.

# line magic


import matplotlib
# matplotlib.use('TkAgg')


import matplotlib.pyplot as plt
plt.ion()


#%matplotlib inline

# Use this when you want the script to be convertable to a python script
try:
    #get_ipython().magic_name("matplotlib inline")
    get_ipython().run_line_magic("matplotlib inline")   #, line, _stack_depth=1)
except:
    plt.ion()
#%%
def get_record(datfile):
    recordname=os.path.basename(datfile).split(".dat")[0]
    recordpath=os.path.dirname(datfile)
    cwd=os.getcwd()
    os.chdir(recordpath) ## somehow it only works if you chdir.
# displays all records in the CHF database
rec_lst = wf.get_record_list('chfdb')   #, records='all')
rec_lst
# Specifies path to data files
path = r'D:\PHD1\pyproj\graph\HRV Data\bidmc-congestive-heart-failure-database-1.0.0\files\chf02'
print(path)
# Slit file name from it's extension
recordname=os.path.basename(path).split(".dat")[0]
print(recordname)
os.path.isfile(recordname)        #(path)     # Checks whether the file exists
# Get the path to the file directory
recordpath=(os.path.dirname(path))
print(recordpath)
# In case you're having trouble with your path specification, run the
# command below to see if path exists.

os.path.exists(recordpath)        #(path)

# Return True if path refers to an existing path or an open file descriptor.
# Returns False for broken symbolic links. On some platforms, this function may return False
# if permission is not granted to execute os.stat() on the requested file, even if the path physically exists.
# pwd   #print working directory
# Print recordname with extension
recordnam=os.path.basename(r'D:\PHD1\pyproj\graph\HRV Data\bidmc-congestive-heart-failure-database-1.0.0\files\chf01.ecg')
print(recordnam)
# Get the last directory name in a path
dirnam = os.path.basename(os.path.dirname(r'D:\PHD1\pyproj\graph\HRV Data\bidmc-congestive-heart-failure-database-1.0.0\files\chf01.ecg'))
print(dirnam)
# absrecordpath=os.path.abspath(recordpath)

## Returns a normalized absolutized version of the pathname path.
## I think instead of using r in front of the path,I could use this.

# print(absrecordpath)
#%%
# Use function to get current working directory
#cwd = os.getcwd()
#cwd
#%%
# Change directory to where the files are saved
os.chdir(recordpath)
#%%
# Get current working directory
cwd=os.getcwd()
print(cwd)
#print ("Current working directory:", os.getcwd())
#%%
# pwd
# Demo 1 - Read a WFDB record using the 'rdrecord' function into a wfdb.Record object.
record = wf.rdrecord(recordname)
# You can also read the same files hosted on PhysioNet https://physionet.org/content/challenge-2015/1.0.0
# in the /training/ database subdirectory.
record_ = wf.rdrecord(recordname, pn_dir='chfdb/1.0.0/')
#%%
# Plot the record
wf.plot_wfdb(record=record, title='Record chf02 From BIDMC Database', return_fig=True)
plt.savefig('t0.png')

## This plots without the annotations and is just used to view the records
# Show the data contained in the record dictionary.
display(record.__dict__)
annotator='ecg'
#%%
# Read a WFDB record and annotation. Plot all channels, and the annotation on top of channel 0.
record2 = wf.rdrecord(recordname, sampto = 15000)  #sampfrom

annotation2 = wf.rdann(recordname, annotator, sampto = 15000)

wf.plot_wfdb(record=record2, annotation=annotation2,
               title='Extract of Record 2 from BIDMC Database',
               time_units='seconds', return_fig=True)
plt.savefig('t1.png')

# Shows annotations for only one channel without symbols
# record5 = wf.rdrecord('chf05')
# annot5 = wf.rdann('chf05','ecg')       #sampfrom=2000, sampto=4000, shift_samps=True)
# display(record5.__dict__)

record5a = wf.rdrecord('chf05', sampfrom=2000, sampto=4000)
annot5a = wf.rdann('chf05', 'ecg', sampfrom=2000, sampto=4000, shift_samps=True,
                   return_label_elements=['symbol'])

wf.plot_wfdb(record=record5a,annotation=annot5a, time_units='seconds', figsize=(10,6),
             ann_style=['r^'], ecg_grids=[0], plot_sym=True, return_fig=True)
plt.savefig('t2.png')

#return_fig=True -> (this will return the figure twice)
# title=None, sig_style=[''], ann_style=['r*'], ecg_grids=[],       # This is the last plot
# Demo 2 - Read certain channels and sections of the WFDB record using the simplified 'rdsamp' function
# which returns a numpy array and a dictionary. Show the data.
signal, field = wf.rdsamp('chf10', sampfrom=6000, sampto=8000)
display(signal)
display(field)
# Can also read the same files hosted on Physionet
signal_, field_ = wf.rdsamp('chf10', channels=[1],
                sampfrom=100, sampto=15000, pn_dir='chfdb/1.0.0/')

display(signal_)
display(field_)
annot_10 = wf.rdann('chf10',annotator, sampfrom=6000, sampto=8000, shift_samps=True,
                    return_label_elements=['symbol'])

wf.plot_items(signal=signal, ann_samp=[annot_10.sample, annot_10.sample],
              ann_sym=[annot_10.symbol, annot_10.symbol],
              title='BIDMC Sample 10: ECG Sample Extract for Channels 1 & 2',
              fs=field['fs'], time_units='seconds', ecg_grids='all',
              sig_name=field['sig_name'],sig_units=field['units'], figsize=(12,8), return_fig=True)
plt.savefig('t3.png')
# Read and plot raw signal of record 4 in chfdb
annot_10a = wf.rdann('chf10',annotator)

signal_10a, field_10a = wf.rdsamp('chf10')

wf.plot_items(signal=signal_10a, ann_samp=[annot_10a.sample, annot_10a.sample],
              title='BIDMC Sample 10: Channels 1 & 2',
              fs=field_10a['fs'], time_units='minutes',
              sig_name=field_10a['sig_name'],sig_units=field_10a['units'],
              figsize=(12,8), return_fig=True)
plt.savefig('t4.png')
help(wf.Annotation)   # this gives the attribute description of the Annotation class.
wf.show_ann_labels()
wf.show_ann_classes()
display(record2.__dict__)
#import time
#from datetime import date
#datetime.time()
#%%
# for loading the whole database
# wf.dl_database('nsrdb', 'data/nsrdb')
print(signal_10a)
# shows number of rows and columns; columns in this case
arr_columns = signal_10a.shape[1]
print(arr_columns)
# import pyhrv
import pyhrv.time_domain as td
import pyhrv.tools as tools
#%%
# Get R-peaks series using biosppy
#t, filtered_signal, rpeaks = biosppy.signals.ecg.ecg(signal_10a)[:3]
t, filtered_signal, rpeaks = ecg.ecg(signal=signal_10a[0:70000,0],
                                     sampling_rate=field_10a['fs'], show=False)[:3]

#%%
display(t, filtered_signal, rpeaks)
output = ecg.ecg(signal=signal_10a[0:70000,0],
                 sampling_rate=field_10a['fs'], show=False)
#%%
# Show 'output' which contains: ts, filtered, rpeaks, templates_ts, templates, heart_rate_ts, and heart_rate
# To access each of these values, type: output['value'] for example.
display(output)
display(output['rpeaks'])
# Compute NNI series. Calculates intervals between the peaks.
nni = tools.nn_intervals(t[rpeaks])
nni
# OPTION 1: Compute Time Domain parameters using the ECG signal
#signal = signal_10a[:,0]
#signal_results = td.time_domain(signal=signal)
# OPTION 2: Compute Time Domain parameters using the R-peak series
rpeaks_results = td.time_domain(rpeaks=t[rpeaks], plot=True, show=True)
plt.savefig('t5.png')
display(rpeaks_results)
# plt.show()
#display(list(rpeaks_results))
# OPTION 3: Compute Time Domain parameters using the NNI-series
# nni_results = td.time_domain(nni=nni, plot=True, show=True)
# plt.show()
# display(nni_results)
