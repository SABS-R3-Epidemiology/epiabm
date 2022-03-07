#
# Decorator to log exceptions in function
#

import logging
from functools import wraps


def log_exceptions(message: str = ""):
    """Provides a try/except clause around the function it is applied to.
    Logs the type of error, and name of the function, if an error occurs,
    with an optional message appended on the end.

    Parameters
    ----------
    message : str
        Optional message to append to default log text

    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logging.exception(f"{type(e).__name__} in "
                                  + f"{func.__qualname__}()" + message)
        return wrapper
    return decorator
