# Question: 
#   Is an song's complexity related to its popularity? 
#
from mrjob.job import MRJob
from mrjob.step import MRStep
import math

header='''artist,title,album,year,duration,artist_familiarity,artist_hotttnesss,song_hotttnesss,artist_terms,artist_terms_freq, artist_terms_weight,mode,key,tempo,loudness,danceabilty,energy,time_signature,segments_start,segments_timbre,segments_pitches,segments_loudness_start,segments_loudness_max,segments_loudness_max_time,sections_start'''.split(",")

class MRCorrHotttnessAverage(MRJob):

    def mapper(self, _, line):
        '''
        For each song, classify the pitches of each segment, determine how 
        complex the song is according to the distribution of its notes,
        and bucket it by the song's hotttnesss score to the nearest 1000th.
        '''
        # try:
        # get pitches of each segment
        pitches = line.split(",")[header.index("segments_pitches")]
        pitches = [x.split(";") for x in pitches.split("_")]
        keys = [0] * 12
        for seg in pitches:
            key = seg.index(max(seg))
            keys[key] += 1

        # normalize counts
        num_segs = len(pitches)
        keys = [(x / num_segs) for x in keys]

        # separate into one of 100 buckets
        try:
            song_hottt = float(line.split(",")[header.index("song_hotttnesss")])
        except:
            song_hottt = float('NaN')
        hottt_bucket = round(song_hottt, 2)

        # shannon's diversity statistic
        num = -sum([x * math.log(x, 2) for x in keys])
        denom = math.log(12, 2)
        if denom < 0.001:
            pass
        else:
            div = num / denom
            yield hottt_bucket, div

        # except:
        #     pass

    def combiner(self, hottt_bucket, div):
        '''
        '''
        print("combiner")
        complexity_list = list(div)
        average_complexity = sum(complexity_list) / len(complexity_list)
        yield None, (hottt_bucket, average_complexity)

    def reducera(self, key, info):
        '''
        '''
        print("reducer")
        yield info[0], info[1]


if __name__ == '__main__':
    MRCorrHotttnessAverage.run()
    

