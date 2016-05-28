#    - len(song_title) ~ song_hotttnesss?
# csv.field_size_limit(sys.maxsize)
#
from mrjob.job import MRJob
from mrjob.step import MRStep
import math
import itertools

class MRCorr(MRJob):

    def steps(self):
        return [
            MRStep( mapper=self.group_by_year,
                    combiner=self.combinations,
                    reducer=self.count_ratings_users_freq)
            ]


    def group_by_year(self, _, line):
        year = int(line.split(",")[3])
        title_len = len(line.split(",")[1])
        song_hotttnesss = float(line.split(",")[7])
        if (year != 0) and (not math.isnan(song_hotttnesss)) and (title_len > 0):
            yield year, (title_len, song_hotttnesss)

            '''
            xx = year * year
            yy = song_hotttnesss * song_hotttnesss
            xy = year * song_hotttnesss
            yield (true, (year, song_hotttnesss, xx, yy, xy, 1))
            '''

    def combinations(self, year, values):
        for song1, song2 in combinations(values, 2):
            (song1_title_len, song1_hotttnesss) = song1
            (song2_title_len, song2_hotttnesss) = song2
            yield (song1_title_len, song2_title_len), \
                    (song1_hotttnesss, song2_hotttnesss)


    def reducer(self, key, values):
        sumx, sumy, sumxx, sumyy, sumxy, n = 0, 0, 0, 0, 0, 0
        for (x, y, xx, yy, xy, counts) in values:
            sumx += x
            sumy += y
            sumxx += xx
            sumyy += yy
            sumxy += xy
            n += counts
        yield n, (sumx, sumy, sumxx, sumyy, sumxy)

    def reducer(self, n, values):
        yield n, values


if __name__ == '__main__':
    MRCorr.run()

