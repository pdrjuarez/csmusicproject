


import subprocess


def run_job(args):
    '''
    input:
        args: list

    output:
        out: list of str
    '''
    args = ["python"] + args
    proc = subprocess.Popen(args, stdout=subprocess.PIPE)
    out = proc.communicate()[0]
    out = out.decode("utf-8")
    # get rid of special characters for clean split
    out = out.translate({ord(i):None for i in '[],'})
    out = out.split()
    return out

def run_corr_hotttnesss(out):
    pass

def go():
    corr_hotttnesss_args = ["corr_hotttnesss.py", "test.csv"]
    corr_hotttnesss = run_jobs(corr_hotttnesss_args)
