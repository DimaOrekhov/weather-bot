from abc import ABC, abstractmethod
import json
from json import JSONDecodeError


class JsonFormatter(ABC):

    @abstractmethod
    def from_json(self, json_string: str):
        pass

    @staticmethod
    def try_get_json(json_string: str):
        try:
            return json.loads(json_string)
        except JSONDecodeError:
            return None


class JsonToTextFormatter(JsonFormatter):

    def from_json(self, json_string: str):
        json_dict = self.try_get_json(json_string)
        if json_dict is None:
            return
        temperature = json_dict['main']['temp']
        return "\n".join([
            f"Температура {temperature} градус{self.get_ending(temperature)} по Цельсию, "
            + f"ощущается как {json_dict['main']['feels_like']}",
            f"Скорость ветра {json_dict['wind']['speed']} метра в секунду",
        ])

    @staticmethod
    def get_ending(num: float) -> str:
        last_digit = int(num) % 10
        if last_digit == 1:
            return ""
        if last_digit in {2, 3, 4}:
            return "а"
        return "ов"
