header='''artist,title,album,year,duration,artist_familiarity,artist_hotttnesss,song_hotttnesss,artist_terms,artist_terms_freq, artist_terms_weight,mode,key,tempo,loudness,danceabilty,energy,time_signature,segments_start,segments_timbre,segments_pitches,segments_loudness_start,segments_loudness_max,segments_loudness_max_time,sections_start'''.split(",")

from mrjob.job import MRJob
from mrjob.step import MRStep
import math

f=open("B_C.csv")
trash=f.readline()
test_song=f.readline().split(",")
test_array=[v.split(";") for v in song[header.index("segments_pitches")].split("_")]
count=0
test_pitches=[]
while count<len(test_array):
    test_pitches.append(count*50)
f.close()

class MRcomparesong(MRJob):

    def mapper(self, _, line):
        song=line.split(",")
        pitch_array=[v.split(";") for v in song[header.index("segments_pitches")].split("_")]
        ##need to define test_Array and test_pitches
        matches=pitch_match(test_array,pitch_array,test_pitches)
        percent_match=percent_match(matches, len(pitch_array))
        if percent_match>0.10:
            song_id="{},{}".format(song[header.index("title"),song[header.index("artist")]])
            yield song_id, percent_match

    def combiner(self, key, vals):
        yield key, list(vals)[0]

    def reducer(self, key, vals):
        yield key, list(vals)[0]

class MatchObject:

    def __init__(self, t0, t1, s0, s1):
        self.t_start=t0
        self.t_finish=t1
        self.s_start=s0
        self.s_finish=s1
    def good_match(self):
        if self.t_finish-self.t_start>=10:
            return True

def percent_match(list_of_match_objects, other_song_num_segments):
    if len(list_of_match_objects)==0:
        return 0
    total_match=0
    for j in list_of_match_objects:
        num_matched_segments=j.s_finish-j.s_start
        total_match+=num_matched_segments/other_song_num_segments
    return total_match/len(list_of_match_objects)

def pitch_match(test_array, song_array, test_pitches):
    rv=[]
    for j in test_pitches:
        starting_rel_pitch=get_relative_pitch(test_array[j], test_array[j+1])
        i=0
        while i < len(song_array)-1:
            rel_pitch=get_relative_pitch(song_array[i], song_array[i+1])
            if starting_rel_pitch==rel_pitch:
                matchobject=Matchobject(j, None, i, None)
                match=True
                test_song_index=j+1
                other_song_index=i+1
                total_tolerance=0
                while match and other_song_index<len(song_array)-1 and test_song_index<len(test_array)-1:
                    if total_tolerance>5:
                        break
                    next_test_rel_pitch=get_relative_pitch(test_array[test_song_index],test_array[test_song_index+1])
                    next_other_song_rel_pitch=get_relative_pitch(song_array[other_song_index],song_array[other_song_index+1])
                    ###This is perfect, continuous match 
                    if next_test_rel_pitch==next_other_song_rel_pitch:
                        test_song_index+=1
                        other_song_index+=1
                    ###woops, next rel. pitches didn't match
                    else:
                        total_tolerance+=1
                        sequential_tolerance=0
                        sequential_counter=1
                        ##match purgatory, you have 5 shots to get a match
                        while match and other_song_index<len(song_array)-6:
                            sequential_counter+=1
                            sequential_tolerance+=1
                            ##Times out, match has ended
                            if sequential_tolerance>5:
                                match=False
                                break
                            next_other_song_rel_pitch=get_relative_pitch(song_array[other_song_index], song_array[other_song_index+sequential_counter])
                            ##break out of match purgatory
                            if next_test_rel_pitch==next_other_song_rel_pitch:
                                test_song_index+=1
                                other_song_index+=sequential_counter
                                break
                            else:
                                continue
                ###Match has ended, we need to store some information about it
                matchobject.t_finish=test_song_index
                matchobject.s_finish=other_song_index
                if matchobject.good_match():
                    rv.append(matchobject)
                i=other_song_index+1
            i+=1
    return rv

def get_relative_pitch(v1, v2):
    try:
        pitch1=v1.index("1.0")
    except:
        max_num=0
        pitch1=None
        for j in range(len):
            if float(v1[j])>max_num:
                max_num=float(v1[j])
                pitch1=j
    try:
        pitch2=v2.index("1.0")
    except:
        max_num=0
        pitch1=None
        for j in range(12):
            if float(v2[j])>max_num:
                max_num=float(v2[j])
                pitch2=j
    if pitch2-pitch1<0:
        return 12-(pitch2-pitch1)
    return pitch2-pitch1


if __name__ == '__main__':
    MRcomparesong.run()

