import time
import threading
from functools import wraps


def rate_limiter(limit_per_sec: int):
    t_lock = threading.Lock()
    limit_per_sec = 9999 if limit_per_sec < 0 else limit_per_sec
    min_interval = 1.0 / limit_per_sec

    def decorate(func):
        last_time_called = time.perf_counter()

        @wraps(func)
        def rate_limiter_func(*args, **kwargs):
            t_lock.acquire()
            nonlocal last_time_called

            try:
                elapsed = time.perf_counter() - last_time_called
                left_to_wait = min_interval - elapsed
                if left_to_wait > 0:
                    time.sleep(left_to_wait)

                return func(*args, **kwargs)
            finally:
                last_time_called = time.perf_counter()
                t_lock.release()

        return rate_limiter_func

    return decorate