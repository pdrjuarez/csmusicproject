from mrjob.job import MRJob
from mrjob.step import MRStep
import math
#header='''artist,title,album,year,duration,artist_familiarity,artist_hotttnesss,song_hotttnesss,artist_terms,artist_terms_freq, artist_terms_weight,mode,key,tempo,loudness,danceabilty,energy,time_signature,segments_start,segments_timbre,segments_pitches,segments_loudness_start,segments_loudness_max,segments_loudness_max_time,sections_start'''.split(",")
class MRCorrHotttnessAverage(MRJob):
    def steps(self):
        return [
            MRStep( mapper=self.mapper,
                    combiner=self.combiner,
                    reducer=self.reducer)
            ]

    def mapper(self, _, line):
       if len(line)>0:
            yield "count",1

    def combiner(self, key, vals):
        yield key, sum(vals)

    def reducer(self, key, vals):
        yield key, sum(vals)

