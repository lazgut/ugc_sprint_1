import time
import logging

from functools import wraps

from flask import current_app

logger = logging.getLogger(__name__)


def backoff(
    start_sleep_time: float | int = 0.1,
    factor: int = 2,
    border_sleep_time: float | int = 10,
):
    def func_wrapper(func):
        @wraps(func)
        def inner(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as error:
                current_app.logger.error(f"Failed {func.__name__} with {str(error)}")
                n = waiting = 0
                while True:
                    try:
                        return func(*args, **kwargs)
                    except Exception as error:
                        current_app.logger.error(f"Failed {func.__name__} with {str(error)}")
                        if waiting < border_sleep_time:
                            n += 1
                            waiting = start_sleep_time * factor**n
                        current_app.logger.warning(
                            f"{func.__name__} restarts after {waiting} seconds"
                        )
                        time.sleep(waiting)

        return inner

    return func_wrapper
