import subprocess
import regression


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


def run_job(args):
    '''
    input:
        args: list

    output:
        out: str
    '''
    args = ["python"] + args
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    out = out.decode("utf-8")
    return out


def run_corr_hotttnesss(out):
    # process output
    out = out.translate({ord(i):None for i in '[],'})
    out = out.split()
    out = [float(x) for x in out]
    # run regression; this could probably be cleaned up lol
    (n, sumx, sumy, sumxx, sumyy, sumxy) = out
    slr = LinearRegression(n, sumx, sumy, sumxx, sumyy, sumxy)
    return slr


def go():
    corr_hotttnesss_args = ["corr_hotttnesss.py", "test.csv"]
    corr_hotttnesss = run_jobs(corr_hotttnesss_args)
