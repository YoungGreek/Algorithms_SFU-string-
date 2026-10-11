import time
from functools import wraps


def log_execution_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed = end - start
        print(f"[LOG] {func.__name__} выполнился за {elapsed:.6f} сек.")
        return result
    return wrapper
