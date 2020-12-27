import re
from typing import Iterable

def get_token(path) -> str:
    with open(path) as istream:
        return istream.read()


API_KEY = get_token("open_weather_token.txt")


def to_full_match_regex(regex_str: str):
    return re.compile(r"^(.*[\s?.,!])?(" + regex_str + r")([\s?.,!].*)?$", re.IGNORECASE)


def or_else(optional, value):
    if optional is None:
        return value
    return optional


def matches_any(query: str, expressions: Iterable[re.Pattern]):
    return any(regex.fullmatch(query) is not None for regex in expressions)
