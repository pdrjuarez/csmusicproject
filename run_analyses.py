# Run_Analyses: Contains classes and functions to make processing
# outputs easier, for testing purposes.
import subprocess
import regression


class Capturing(list):
    '''
    A context manager to capture stdout from a python function call,
    as a python variable that can then be manipulated as a string.
    
    Usage:
        with Capturing() as output:
            do_something(my_object)
            
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
    A function to run a python script within python in exactly the same way
    you would run it using a bash command, and return the stdout output
    as a variable.
    
    input:
        args: list of str, such as:
            ["script.py", "arg1", "arg2"]

    output:
        out: str
    '''
    args = ["python"] + args
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    out = out.decode("utf-8")
    return out


def run_regression(out):
    '''
    Quickly tests the above on regression.py, for viability.
    '''
    # process output
    out = out.translate({ord(i):None for i in '[],'})
    out = out.split()
    out = [float(x) for x in out]
    # run regression
    (n, sumx, sumy, sumxx, sumyy, sumxy) = out
    slr = LinearRegression(n, sumx, sumy, sumxx, sumyy, sumxy)
    return slr


def go():
    corr_hotttnesss_args = ["corr_hotttnesss.py", "test.csv"]
    corr_hotttnesss = run_jobs(corr_hotttnesss_args)
