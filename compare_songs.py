###File to compare a test song to all the other songs in the dataset
###Currently, does not have a nice way to receive the test song as an input, 
###because our csv_files don't allow for easy searching of a particular song
###The input is therefore a csv file (e.g "B_A.csv"), 
###and a line number (1- (#lines in csv file) -1), representing the song you want to test
###see bottom for usage

header='''artist,title,album,year,duration,artist_familiarity,artist_hotttnesss,song_hotttnesss,artist_terms,artist_terms_freq, artist_terms_weight,mode,key,tempo,loudness,danceabilty,energy,time_signature,segments_start,segments_timbre,segments_pitches,segments_loudness_start,segments_loudness_max,segments_loudness_max_time,sections_start'''.split(",")

from mrjob.job import MRJob
from mrjob.step import MRStep
import math

class MRcomparesong(MRJob):

    def mapper(self, _, line):
        '''We're just using MRJob as a way to distribute work, so this is the only thing that's interesting'''
        ##catch the header
        if line[:12]!="artist,title":    
            song=line.split(",")
            pitch_array=[v.split(";") for v in song[header.index("segments_pitches")].split("_")]
            duration=song[header.index("duration")]
            segments_start_array=song[header.index("segments_start")].split("_")
            matches=pitch_match(test_array,pitch_array,test_pitches)
            per_cent_match=percent_match(matches, segments_start_array,duration)
            #Any meaningful match whatsoever, yield it
            if per_cent_match>0:
                song_id="{},{}".format(song[header.index("title"),song[header.index("artist")]])
                print("I'm yielding something!")
                yield song_id, per_cent_match

    def combiner(self, key, vals):
        '''Each key is 'title,artist', and is only yielded 1 or 0 times, therefore we don't really do much here
        print("combiner", key)
        yield key, list(vals)[0]

    def reducer(self, key, vals):
        '''Same here'''
        print("reducer", key)
        yield key, list(vals)[0]

class MatchObject:
    '''Contains information about a matching sequence of segments (matching melody) between two songs'''
    def __init__(self, t0, t1, s0, s1):
        #All these are segment indicators, e.g. t0=400, t1=500 means the test song's match is from segment 400 to 500
        #s0 and s1 are similar, but for the other song being tested against. 
        self.t_start=t0
        self.t_finish=t1
        self.s_start=s0
        self.s_finish=s1
    def good_match(self):
        '''Basically a way to remove matches that don't last very long in number of segments. We don't care whether
        the test song has a relative fourth pitch because likely every song has a relative fourth pitch -- the melody is captured
        by a sequence of these relative pitches. 10 is probably too big, though, can change.
        We also count the number of segments matched of the test song because we care about how much of the test song's melody 
        is found in other songs to decide whether it's a good match. The number of segments this match spans in the other song 
        is used to determine the percent match'''
        if self.t_finish-self.t_start>=10:
            return True

def percent_match(list_of_match_objects, other_song_segments_start, other_song_duration):
    '''A way to come up with percent match between a song and the test song
    For each match object, looks at what percent of the other song is taken from the test_song, measured in seconds
        Input: list_of_match_objects, a list of MatchObject
               other_song_segments_start, an array of strings (later converted to floats) each marking the time in seconds of the start of a segment
               other_song_duration, string in seconds
               
        Output: A float between 0 and 1 ,representing the amount of time that the other song's melodies are similar to the test song's melodies'''
    if len(list_of_match_objects)==0:
        return 0
    total_match=0
    for j in list_of_match_objects:
        ###overlapping matches?
        matched_time=float(other_song_segments_start[j.s_finish])-float(other_song_segments_start[j.s_start])
        total_match+=matched_time
    return total_match/other_song_duration

def pitch_match(test_array, song_array, test_pitches):
    '''Our algorithm for comparing melodies. We don't look at pitches thesmelves, instead the relative pitches moving from one
    segment to the next. This hopefullly catches melodies that have been transposed up or down in another song'''
        Input: test_array, the test_songs array of pitches for each segment
               song_array, the other songs's array of pitches for each segment
               test_pitches, the segment numbers we start looking for matches at in the test_song
        
        Output: A list of match objects, each containing information about a significant match found between both pitch arrays'''
    rv=[]
    for j in test_pitches:
        ##We decide to start looking for similarities at all of these points
        starting_rel_pitch=get_relative_pitch(test_array[j], test_array[j+1])
        i=0
        #we search for this relative pitch throughout the entire other song
        while i < len(song_array)-1:
            rel_pitch=get_relative_pitch(song_array[i], song_array[i+1])
            #as soon as we find a match, we continue looking for similarities until they're too far apart in melody
            if starting_rel_pitch==rel_pitch:
                matchobject=MatchObject(j, None, i, None)
                match=True
                test_song_index=j+1
                other_song_index=i+1
                #total_tolerance is the amount of 'mistakes' the other song has made so far, where the 'correct' version is the test_song's melody
                total_tolerance=0
                #don't want indexing errors
                while match and other_song_index<len(song_array)-1 and test_song_index<len(test_array)-1:
                    #amount of mistakes we'll tolerate before we quit looking
                    if total_tolerance>5:
                        break
                    next_test_rel_pitch=get_relative_pitch(test_array[test_song_index],test_array[test_song_index+1])
                    next_other_song_rel_pitch=get_relative_pitch(song_array[other_song_index],song_array[other_song_index+1])
                    ##This is the ideal case, relative pitches continue to match
                    if next_test_rel_pitch==next_other_song_rel_pitch:
                        test_song_index+=1
                        other_song_index+=1
                    ##woops, the next relative pitches didn't match. Add up one mistake
                    else:
                        ###At this point, we recognize that a cover song might have things like extra notes or slight changes to the melody
                        ###For example, the original melody might have gone CEGGEC, and I copied it as CEGFGEC, adding an F as a decoration note
                        ###In this block, we allow for some amount of 'sequential mistakes', where the other song is allowed a number of mistakes in 
                        ###succession before quitting the match. If it manages to re-sync up with the test_song's melody before that, it backs out into the 
                        ###outer while loop
                        total_tolerance+=1
                        sequential_tolerance=0
                        sequential_counter=1
                        #avoid index errors
                        while match and other_song_index<len(song_array)-6:
                            sequential_counter+=1
                            sequential_tolerance+=1
                            ##Too many sequential mistakes, exit out of both while loops
                            ##match=False breaks me out of the outer loop.
                            if sequential_tolerance>4:
                                match=False
                                break
                            next_other_song_rel_pitch=get_relative_pitch(song_array[other_song_index], song_array[other_song_index+sequential_counter])
                            ##we resynced back up with the test song, break out of this while loop
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
    '''Given two pitch vectors v1 and v2, find the relative pitch moving from v1 to v2, where we only look at the most important (loudest) coordinate
    The information given to us in this dataset doesn't really let this be accurate, because each vector 
    is only 12 coordinates for the relative presence of each of the 12 pure tones in that segment. Thus, it does not
    contain information about which octave we are in, so going from C to G could be going up a 5th or down a fourth
    Here we assume that we're always going up in pitch, to normalize things'''
    try:
        #most of these pitch vectors have the loudest tone as 1.0
        pitch1=v1.index("1.0")
    except:
        max_num=0
        pitch1=None
        for j in range(12):
            print(v1[j])
            if float(v1[j])>max_num:
                max_num=float(v1[j])
                pitch1=j
    try:
        pitch2=v2.index("1.0")
    except:
        max_num=0
        pitch2=None
        for j in range(12):
            if float(v2[j])>max_num:
                max_num=float(v2[j])
                pitch2=j
    if pitch2-pitch1<0:
        return 12-(pitch2-pitch1)
    return pitch2-pitch1


if __name__ == '__main__':
    print("here")
    f=open("A_A.csv")
    trash=f.readline() #header
    test_song=f.readline().split(",")
    test_array=[v.split(";") for v in test_song[header.index("segments_pitches")].split("_")]
    count=0
    test_pitches=[]
    print("all the way")
    while count<len(test_array):
        test_pitches.append(count)
        count+=50
    f.close()
    print("we made it")
    MRcomparesong.run()

