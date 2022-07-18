from pathlib import Path
from http.cookies import SimpleCookie


def parse_cookie(raw_cookie: str) -> dict[str, str]:
    """Parse a raw cookie string into a dictionnary."""
    cookie_parser = SimpleCookie()
    cookie_parser.load(raw_cookie)
    return {k: v.value for k, v in cookie_parser.items()}


def get_src_path() -> Path:
    """Return the absolute path of the source folder."""
    return (Path(__file__).parent.parent).resolve()