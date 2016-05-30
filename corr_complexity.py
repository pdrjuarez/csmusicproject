# Question: 
#   Is an song's complexity related to its popularity? 
#
from mrjob.job import MRJob
from mrjob.step import MRStep
import math
from scipy.stats import t

from io import StringIO
import sys

header='''artist,title,album,year,duration,artist_familiarity,artist_hotttnesss,song_hotttnesss,artist_terms,artist_terms_freq, artist_terms_weight,mode,key,tempo,loudness,danceabilty,energy,time_signature,segments_start,segments_timbre,segments_pitches,segments_loudness_start,segments_loudness_max,segments_loudness_max_time,sections_start'''.split(",")

class MRCorrHotttnessAverage(MRJob):

    def steps(self):
        return [
            MRStep( mapper=self.mappera,
                    combiner=self.combinera,
                    reducer=self.reducera)
            ]

    def mappera(self, _, line):
        '''
        For each song, classify the pitches of each segment, determine how 
        complex the song is according to the distribution of its notes,
        and bucket it by the song's hotttnesss score to the nearest 1000th.
        '''
        try:
            # get pitches of each segment
            pitches = line.split(",")[header.index("segments_pitches")]
            pitches = [x.split(";") for x in pitches.split("_")]
            keys = [0] * 12
            for seg in pitches:
                key = seg.index("1.0")
                keys[key] += 1

            # normalize counts
            num_segs = len(pitches)
            keys = [(x / num_segs) for x in keys]

            # separate into one of 1000 buckets
            song_hottt = float(line.split(",")[header.index("song_hotttnesss")])
            hottt_bucket = round(song_hottt, 3)

            # shannon's diversity statistic
            div = -sum([x * math.log(x, 2) for x in norm_keys]) / math.log(12, 2)

            yield hottt_bucket, div

        except:
            pass

    def combinera(self, hottt_bucket, complexity):
        '''
        '''
        complexity_list = list(complexity)
        average_complexity = sum(complexity) / len(complexity)
        yield None, (hottt_bucket, average_complexity)

    def reducera(self, key, info):
        '''
        '''
        yield info[0], info[1]


class Capturing(list):
    '''
    http://stackoverflow.com/questions/16571150/how-to-capture-stdout-output-from-a-python-function-call
    '''
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self

    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        sys.stdout = self._stdout


if __name__ == '__main__':
    with Capturing() as output:
        MRCorrHotttnessAverage.run()
    

