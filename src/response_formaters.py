from abc import ABC, abstractmethod
import json
from json import JSONDecodeError
import datetime


class JsonFormatter(ABC):

    @abstractmethod
    def from_json(self, json_string: str, city: str, date_offset: int):
        pass

    @staticmethod
    def try_get_json(json_string: str):
        try:
            return json.loads(json_string)
        except JSONDecodeError:
            return None


class JsonToTextFormatter(JsonFormatter):

    MONTHS = [
        'января', 'февраля', 'марта',
        'апреля', 'мая', 'июня',
        'июля', 'августа', 'сентября',
        'октября', 'ноября', 'декабря'
    ]

    def from_json(self, json_string: str, city: str, date_offset: int):
        json_dict = self.try_get_json(json_string)
        if json_dict is None:
            return
        city_string = 'Санкт-Петербурге' if city == 'Saint Petersburg' else 'Москве'
        date = datetime.datetime.today() + datetime.timedelta(days=date_offset)
        date_string = f"{date.day} {JsonToTextFormatter.MONTHS[date.month - 1]}"
        weather_dict = json_dict['daily'][date_offset]
        return "\n".join([
            f"Погода в {city_string} {date_string}:\n",
            f"{weather_dict['weather'][0]['description'].capitalize()}.\n",
            JsonToTextFormatter.temp_string_at_time(
                "утром",
                weather_dict["temp"]["morn"],
                weather_dict["feels_like"]["morn"]
            ),
            JsonToTextFormatter.temp_string_at_time(
                "днем",
                weather_dict["temp"]["day"],
                weather_dict["feels_like"]["day"]
            ),
            JsonToTextFormatter.temp_string_at_time(
                "вечером",
                weather_dict["temp"]["eve"],
                weather_dict["feels_like"]["eve"]
            ),
            JsonToTextFormatter.temp_string_at_time(
                "ночью",
                weather_dict["temp"]["night"],
                weather_dict["feels_like"]["night"]
            ),
            f"Скорость ветра {weather_dict['wind_speed']} метра в секунду.",
            f"Влажность {weather_dict['humidity']}%."
        ])

    @staticmethod
    def temp_string_at_time(when, temperature, feels_like):
        return f"Температура {when} {temperature} градус{JsonToTextFormatter.get_ending(temperature)} по Цельсию, " \
            + f"ощущается как {feels_like}.\n"

    @staticmethod
    def get_ending(num: float) -> str:
        last_digit = int(num) % 10
        if last_digit == 1:
            return ""
        if last_digit in {2, 3, 4}:
            return "а"
        return "ов"
