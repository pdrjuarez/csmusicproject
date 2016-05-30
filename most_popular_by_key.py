# Question: 
#   Which songs are most popular in each key?
#
from mrjob.job import MRJob
from mrjob.step import MRStep
import math
from scipy.stats import t

header='''artist,title,album,year,duration,artist_familiarity,artist_hotttnesss,song_hotttnesss,artist_terms,artist_terms_freq, artist_terms_weight,mode,key,tempo,loudness,danceabilty,energy,time_signature,segments_start,segments_timbre,segments_pitches,segments_loudness_start,segments_loudness_max,segments_loudness_max_time,sections_start'''.split(",")

class MRMostPopularByKey(MRJob):

    def mapper(self, _, line):
        '''
        For each song, emits the key and song's basic info (title, artist, hotttnesss)
        '''
        try:
            line = line.split(",")
            song_hottt = float(line[header.index("song_hotttnesss")])
            key = int(line[header.index("key")])
            title = line[header.index("title")]
            artist = line[header.index("artist")]
            if (not math.isnan(song_hottt)):
                yield key, (title, artist, song_hottt)

        except:
            pass

    def combiner(self, key, info):
        for (title, artist, song_hottt) in info:
            yield key, (title, artist, song_hottt)

    def reducer_init(self):
        '''
        Initializes vars to store information about the most popular songs
        '''
        self.most_popular_title = [None] * 12
        self.most_popular_artist = [None] * 12
        self.most_popular_score = [0.0] * 12

        self.temp_most_popular_title = None
        self.temp_most_popular_artist = None
        self.temp_most_popular_score = 0.0

    def reducer(self, key, song_info):
        '''
        For each key, goes through songs to find the most popular one
        '''
        print("key")
        for song, artist, hotttnesss in song_info:
            if hotttnesss > self.temp_most_popular_score:
                self.temp_most_popular_score = hotttnesss
                self.temp_most_popular_title = song
                self.temp_most_popular_artist = artist
        # store finalists in list
        self.most_popular_title[key] = self.temp_most_popular_title
        self.most_popular_artist[key] = self.temp_most_popular_artist
        self.most_popular_score[key] = self.temp_most_popular_score
        # reset values for next key
        self.temp_most_popular_title = None
        self.temp_most_popular_artist = None
        self.temp_most_popular_score = 0.0

    def reducer_final(self):
        '''
        Yields results in a readable format
        '''
        keys = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        for i in range(12):
            key = keys[i]
            title = self.most_popular_title[i]
            artist = self.most_popular_artist[i]
            score = self.most_popular_score[i]
            yield keys[i], "{}, by {}, {}".format(title, artist, score)


if __name__ == '__main__':
    MRMostPopularByKey.run()

