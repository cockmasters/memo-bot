from datetime import datetime
import time
from functools import wraps


def async_timeit(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        end = time.perf_counter()
        print(f'{func.__name__} took {end - start:.6f} seconds to complete')
        return result

    return wrapper


def time_of_completion(fun):
    @wraps(fun)
    async def wrapped(*args):
        t = datetime.now()
        res = await fun(*args)
        print(datetime.now() - t)
        return res

    return wrapped
