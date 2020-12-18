import json

from src.weather_bot import weather_bot


def get_token(path):
    with open(path) as istream:
        return istream.read()


def get_city_id_map(path):
    with open(path) as istream:
        cities = json.load(istream)
    return {c['name']: c['id'] for c in cities}, {c['name']: c for c in cities}


if __name__ == "__main__":
    weather_bot.polling(none_stop=True, interval=0)
