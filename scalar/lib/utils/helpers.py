import time
from typing import Callable, Any
from functools import wraps

def retry(max_attempts: int = 3, delay: int = 5, exceptions: tuple = (Exception,)):
    """Retry decorator"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        time.sleep(delay)
                        continue
                    raise last_exception
            return wrapper
        return wrapper

def timeout(seconds: int):
    """Timeout decorator"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            import signal
            
            def _timeout_handler(signum, frame):
                raise TimeoutError(f"Function {func.__name__} timed out after {seconds} seconds")
            
            signal.signal(signal.SIGALRM, _timeout_handler)
            signal.alarm(seconds)
            
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            
            return result
        return wrapper
