# Question: 
#   Does an artist's hotttnesss affect their average song hotttnesss? 

from mrjob.job import MRJob
from mrjob.step import MRStep
import math

class MRCorr(MRJob):

    def mapper(self, _, line):
        '''
        '''
        try:
            artist = line.split(",")[0]
            artist_hottt = float(line.split(",")[6])
            song_hottt = float(line.split(",")[7])
            if (not math.isnan(artist_hottt)) and (not math.isnan(song_hottt)):
                yield (artist, artist_hottt), song_hottt
        except:
            pass

    def combiner(self, artist_info, songs):
        '''
        '''
        (artist, artist_hottt) = artist_info
        songs_info = list(songs)
        average_song_hottt = sum(songs_info) / len(songs_info)
        yield True, (artist_hottt, average_song_hottt)

    def reducer(self, key, hottt_info):
        '''
        '''
        sumx, sumy, sumxx, sumyy, sumxy, n = (0.0, 0.0, 0.0, 0.0, 0.0, 0)
        for (x, y) in hottt_info:
            sumx += x
            sumy += y
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
            n += 1
        yield n, (sumx, sumy, sumxx, sumyy, sumxy)

if __name__ == '__main__':
    MRCorr.run()

