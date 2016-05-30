from mrjob.job import MRJob
from mrjob.step import MRStep
import math

header='''artist,title,album,year,duration,artist_familiarity,artist_hotttnesss,song_hotttnesss,artist_terms,artist_terms_freq, artist_terms_weight,mode,key,tempo,loudness,danceabilty,energy,time_signature,segments_start,segments_timbre,segments_pitches,segments_loudness_start,segments_loudness_max,segments_loudness_max_time,sections_start'''.split(",")

class MRCount(MRJob):

    def mapper(self, _, line):
        try:
            year = int(line.split(",")[header.index("year")])
            if True:
            # if year > 0:
                yield None, 1
        except:
            pass

    def reducer(self, _, vals):
        yield None, sum(vals)


if __name__ == '__main__':
    MRCount.run()

