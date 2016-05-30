# Question: 
#   Is an artist's hotttnesss related to their average song hotttnesss? 
#
from mrjob.job import MRJob
from mrjob.step import MRStep
import math
from scipy.stats import t

header='''artist,title,album,year,duration,artist_familiarity,artist_hotttnesss,song_hotttnesss,artist_terms,artist_terms_freq, artist_terms_weight,mode,key,tempo,loudness,danceabilty,energy,time_signature,segments_start,segments_timbre,segments_pitches,segments_loudness_start,segments_loudness_max,segments_loudness_max_time,sections_start'''.split(",")

class MRCorrHotttnessAverage(MRJob):

    def steps(self):
        return [
            MRStep( mapper=self.group_by_artist,
                    combiner=self.put_all_together,
                    reducer=self.regression_analysis)
            ]

    def group_by_artist(self, _, line):
        '''
        For each artist, yield their hottnesss and all their song's hotttnesses
        '''
        try:
            artist = line.split(",")[header.index("artist")]
            artist_hottt = float(line.split(",")[header.index("artist_hotttnesss")])
            song_hottt = float(line.split(",")[header.index("song_hotttnesss")])
            if (not math.isnan(artist_hottt)) and (not math.isnan(song_hottt)):
                yield (artist, artist_hottt), song_hottt
        except:
            pass

    def put_all_together(self, artist_info, songs):
        '''
        Yield (x, y) pairs where x = artist_hottt and y=average_song_hottt.
        In other words, an artist's hotttnesss is our predictor variable,
        and the average song hotttnesss is our response variable.
        '''
        (artist, artist_hottt) = artist_info
        songs_info = list(songs)
        average_song_hottt = sum(songs_info) / len(songs_info)
        yield True, (artist_hottt, average_song_hottt)

    def regression_analysis(self, key, info):
        '''
        Calculates all the values we will need for simple linear regression 
        analysis, and does the analysis itself.
        '''
        # not the most efficient, but we want to keep these values
        # to calculate standard errors
        info = list(info)

        # calculate sums
        sumx, sumy, sumxx, sumyy, sumxy, n = (0.0, 0.0, 0.0, 0.0, 0.0, 0)
        for (x, y) in info:
            sumx += x
            sumy += y
            sumxx += x * x
            sumyy += y * y
            sumxy += x * y
            n += 1

        # calculate correlation
        corr = 0
        corr_denom = math.sqrt((n * sumxx - sumx**2) * (n * sumyy - sumy**2))
        if corr_denom < 0.0001:
            yield False, "Could not calculate coefficients"

        corr_num = n * sumxy - sumx * sumy 
        corr = corr_num / corr_denom

        if abs(corr) < 0.0001:
            yield False, "Could not calculate coefficients"

        # calculate regression coefficients
        beta1 = (sumxy - sumx * sumy / n) / (sumxx - sumx**2 / n)
        beta0 = (sumy - beta1 * sumx) / n

        # calculate standard errors
        y_reals = [y for (x, y) in info]
        y_hats = [beta0 + beta1 * y for y in y_reals]
        s_num = sum([(y - yhat) for (y, yhat) in zip(y_reals, y_hats)])
        s = math.sqrt(s_num / (n - 2))

        se_denom = n * sumxx - sumx**2
        se_beta0 = s * math.sqrt(sumxx / se_denom)
        se_beta1 = s * math.sqrt(n / se_denom)

        # calculate t-values
        t0 = beta0 / se_beta0
        t1 = beta1 / se_beta1

        # calculate 2-sided p-values
        alpha = 0.05
        t_stat = t.ppf(1 - alpha/2, n - 2)
        beta0_p_value = t.sf(abs(t0), n - 2) * 2
        beta1_p_value = t.sf(abs(t1), n - 2) * 2

        yield (beta0, se_beta0, t0, beta0_p_value), \
                (beta1, se_beta1, t1, beta1_p_value)


if __name__ == '__main__':
    MRCorrHotttnessAverage.run()

