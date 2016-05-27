#usual imports
import os
import sys
import time
import glob
import datetime
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
header='''artist,title,album,year,duration,artist_familiarity,artist_hotttnesss,song_hotttnesss,artist_terms,artist_terms_freq, artist_terms_weight,mode,key,tempo,loudness,danceabilty,energy,time_signature,segments_start,segments_timbre,segments_pitches,segments_loudness_start,segments_loudness_max,segments_loudness_max_time,sections_start\n'''

def csv_convert(basedir, csv_filename):
	t1=time.time()
	cnt=0
	with open("/home/ec2-user/{}".format(csv_filename), "w") as csv_file:
		csv_file.write(header)
		for root, dirs, files in os.walk(basedir):
			files=glob.glob(os.path.join(root, '*.h5'))
			for f in files:
				h5=gt.open_h5_file_read(f)
				num_songs=gt.get_num_songs(h5)
				for j in range(int(num_songs)):
					if validate_song(h5, j):
						cnt+=1
						csv_file.write(h5_to_csv_fields(h5,j))
						if cnt%10==0:
							print("{} files csved thus far".format(cnt))
				h5.close()
	t2=time.time()
	print ('directory {} csv-ed in:'.format(basedir), strtimedelta(t1,t2))

def h5_to_csv_fields(h5,song):
	rv=[]
	rv.append(gt.get_artist_name(h5,song))
	rv.append(gt.get_title(h5, song))
	rv.append(gt.get_release(h5, song))
	rv.append(gt.get_year(h5,song))
	rv.append(gt.get_duration(h5,song))
	rv.append(gt.get_artist_familiarity(h5,song))
	rv.append(gt.get_artist_hotttnesss(h5,song))
	rv.append(gt.get_song_hotttnesss(h5, song))
	rv.append(array_to_csv_field(list(gt.get_artist_terms(h5,song))))
	rv.append(array_to_csv_field(list(gt.get_artist_terms_freq(h5,song))))
	rv.append(array_to_csv_field(list(gt.get_artist_terms_weight(h5,song))))
	rv.append(gt.get_mode(h5,song))
	rv.append(gt.get_key(h5,song))
	rv.append(gt.get_tempo(h5,song))
	rv.append(gt.get_loudness(h5,song))
	rv.append(gt.get_danceability(h5,song))
	rv.append(gt.get_energy(h5,song))
	rv.append(gt.get_time_signature(h5,song))
	rv.append(array_to_csv_field(list(gt.get_segments_start(h5,song))))
	##These arrays have vectors (Arrays) as items, 12 dimensional each
	##For now, an array like [[1,2,3],[4,5,6]] will be written to csv as '1;2;3_4;5;6'
	#not sure this is efficient on the csv side

	rv.append(double_Array_to_csv_field(list(gt.get_segments_timbre(h5,song)),'_',';'))
	rv.append(double_Array_to_csv_field(list(gt.get_segments_pitches(h5,song)),'_',';'))

	rv.append(array_to_csv_field(list(gt.get_segments_loudness_start(h5,song))))
	rv.append(array_to_csv_field(list(gt.get_segments_loudness_max(h5,song))))
	rv.append(array_to_csv_field(list(gt.get_segments_loudness_max_time(h5,song))))
	rv.append(array_to_csv_field(list(gt.get_sections_start(h5,song))))
	rv_string=array_to_csv_field(rv, ",")
	rv_string+="\n"
	return rv_string

def array_to_csv_field(array, char="_"):
	rv=str(array[0])
	for j in array[1:]:
		rv+=char
		rv+=str(j)
	return rv

def double_Array_to_csv_field(double_array, char1, char2):

	rv=str(array_to_csv_field(double_array[0], char2))
	for j in double_array[1:]:
		rv+=char1
		rv+=str(array_to_csv_field(j,char2))
	return rv


def validate_song(h5_file,song):
	'''Returns true/false if song is valid or not'''
	try:
		assert gt.get_year(h5_file, song)!='0'
		assert gt.get_duration(h5_file, song)>60.0
		assert gt.get_mode_confidence(h5_file, song)>0.2
		assert gt.get_key_confidence(h5_file, song)>0.2
		assert gt.get_time_signature_confidence(h5_file, song)>0.2
		terms=np.array(gt.get_artist_terms(h5_file, song))
		assert terms.size>0
		segments=np.array(gt.get_segments_start)
		assert segments.size>0
		sections=np.array(gt.get_sections_start)
		assert sections.size>0
	except:
		return False
	return True

def strtimedelta(starttime,stoptime):
    return str(datetime.timedelta(seconds=stoptime-starttime))

def apply_to_all_files(basedir, func=lambda x: x):
	"""
	   From a base directory, go through all subdirectories,
	   find all files with the given extension, apply the
	   given function 'func' to all of them.
	   If no 'func' is passed, we do nothing except counting.
	   INPUT
	      basedir  - base directory of the dataset
	      func     - function to apply to all filenames
	      ext      - extension, .h5 by default
	   RETURN
	      number of files
	"""
	cnt = 0
	# iterate over all files in all subdirectories
	for root, dirs, files in os.walk(basedir):
	    files = glob.glob(os.path.join(root,'*.h5'))
	    # count files
	    cnt += len(files)
	    # apply function to all files
	    for f in files :
	        func(f)       
	return cnt

if __name__ == '__main__':
	usage = "python csvify.py <subdirectory> <csv_filename>\n. Example use: csvify.py 'A/A/A' A_A_A.csv"
	args_len=len(sys.argv)
	if args_len==3:
		sub_dir=str(sys.argv[1])
		csv_filename=str(sys.argv[2])
		basedir=os.path.join(data_path, sub_dir)
		if not os.path.isdir(basedir):
			print ("{} not a valid directory".format(basedir))
			print(usage)
			sys.exit(0)

		else:
			csv_convert(basedir, csv_filename)
	else:
		print(usage)
		sys.exit(0)
