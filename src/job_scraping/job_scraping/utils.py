import functools
import logging
from pathlib import Path
from typing import Callable
from http.cookies import SimpleCookie


def parse_cookie(raw_cookie: str) -> dict[str, str]:
    """Parse a raw cookie string into a dictionnary."""
    cookie_parser = SimpleCookie()
    cookie_parser.load(raw_cookie)
    return {k: v.value for k, v in cookie_parser.items()}


def get_src_path() -> Path:
    """Return the absolute path of the source folder."""
    return (Path(__file__).parent.parent).resolve()


def to_snake_case(camel_str: str) -> str:
    return ''.join(['_' + c.lower() if c.isupper() else c for c in camel_str]).lstrip('_')


def logged(func: Callable) -> Callable:
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            logging.debug(f'Executing {func.__name__} with args {args}')
            return result
        except Exception as err:
            logging.exception(f'Exception raised in {func.__name__}: {err}')
            raise err

    return wrapper
