'''
Module errors provides decorators and functions to log and display errors
consistently during program execution.
'''

from functools import wraps
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional
from display_utils import colorize


BASE_DIR = Path(__file__).resolve().parent.parent
LOG_DIR = BASE_DIR / 'logs'
LOG_FILE = LOG_DIR / 'error.log'

def log_error_to_file(message: str) -> None:
    '''
    Writes an error message to the log file with a timestamp.
    '''
    LOG_DIR.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f'[{timestamp}] {message}\n')


def show_error(message: str) -> None:
    '''
    Displays an error message in red color in the console.
    '''

    print(colorize(message, 'red'))


def log_error(display: bool = True, rethrow: bool = False) -> Callable:
    '''
    Decorator for logging exceptions during function execution.

    Args:
        display (bool): Show error message in console.
        rethrow (bool): Re-raise exception after logging.

    Returns:
        Callable: Wrapped function.
    '''

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_message = (
                    f'{type(e).__name__} in {func.__name__}: {e}'
                )
                log_error_to_file(error_message)

                if display:
                    show_error(f'Error: {e}')

                if rethrow:
                    raise

                return None

        return wrapper

    return decorator