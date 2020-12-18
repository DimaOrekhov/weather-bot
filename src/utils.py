def get_token(path) -> str:
    with open(path) as istream:
        return istream.read()


API_KEY = get_token("../open_weather_token.txt")
