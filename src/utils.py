import re


def get_token(path) -> str:
    with open(path) as istream:
        return istream.read()


API_KEY = get_token("open_weather_token.txt")


def to_full_match_regex(regex_str: str):
    return re.compile(r"^(.*[\s?.,!])?(" + regex_str + r")([\s?.,!].*)?$", re.IGNORECASE)
