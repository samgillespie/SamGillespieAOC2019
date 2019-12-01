import datetime

def timeit(method):
    def timed(*args, **kw):
        tic = datetime.datetime.now()
        results = method(*args, **kw)
        toc = datetime.datetime.now()
        elapsed_time = toc-tic
        print(elapsed_time.total_seconds())
        return results
    return timed
