#    - len(song_title) ~ song_hotttnesss?
# csv.field_size_limit(sys.maxsize)
#
from mrjob.job import mrjob


class MRCorr(MRJob):

    def mapper(self, _, line):
        year = line.split(",")[3]
        song_hotttnesss = line.split(",")[7]
        yield year, song_hotttnesss

    def combiner(self, name, counts):
        yield name, sum(counts)

    def reducer(self, name, counts):
        count = sum(counts)
        if count >= 10:
            yield name, count
            # yield key, (suml, sumh, sumxy, sumxx, sumyy)



if __name__ == '__main__':
    MRTenVisits.run()

