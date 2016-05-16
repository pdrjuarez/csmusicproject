#usual imports
import os
import sys
import time
import glob
import dateimt
import sqlite3
import csv
import numpy as np
#path to the dataset
path='/mnt/music'
assert os.path.isdir(path), 'Expected path /mnt/music'
data_path=os.path.join(path, 'data')
extrastuff_path=os.path.join(path, 'AdditionalFiles')
#path to the wrapper code
code_path='MSongsDB'
assert os.path.isdir(code_path), 'Expected path MSongsDB'
sys.path.append(os.path.join(code_path, 'PythonSrc'))

import hdf5_getters as gt


def validate_song(filename):
	'''Returns true/false if song is valid or not'''

def convert_to_csv(basedir):

