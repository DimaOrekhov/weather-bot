from collections import defaultdict
from abc import ABC, abstractmethod
import requests
from typing import Optional, Callable, Tuple

from src.utils import API_KEY


class DialogContext(ABC):

    @abstractmethod
    def get_response(self) -> Tuple[bool, str]:
        pass

    @abstractmethod
    def update(self, new_context: 'DialogContext') -> 'DialogContext':
        pass

    @abstractmethod
    def is_complete(self) -> bool:
        pass


class WeatherReportContext(DialogContext):

    AVAILABLE_CITIES = (
        'Saint Petersburg',
        'Moscow'
    )

    def __init__(
            self,
            city_name: Optional[str] = None,
            state_code: Optional[str] = None,
            date: Optional[str] = None
    ):
        self.city_name = city_name
        self.state_code = state_code
        self.date = date

    def get_response(self) -> Tuple[bool, str]:
        if self.city_name is None:
            return False, "Уточните, пожалуйста, город"

        if self.date is None:
            return False, "Уточните, пожалуйста, дату желаемого прогноза"

        if self.city_name not in WeatherReportContext.AVAILABLE_CITIES:
            return True, "Погода в данном месте мне неизвестна"

        payload = {
            'q': f'{self.city_name},{self.state_code}',
            'appid': API_KEY,
            'units': 'metric'
        }
        response = requests.get(
            f"https://api.openweathermap.org/data/2.5/weather", params=payload
        )
        return True, response.text

    @staticmethod
    def json_to_user_answer(json_string: str) -> str:
        pass

    def update(self, new_context: DialogContext) -> DialogContext:
        if not isinstance(new_context, WeatherReportContext):
            raise TypeError("Can update only with the context of the same type")

        self.city_name = self.city_name or new_context.city_name
        self.state_code = self.state_code or new_context.state_code
        self.date = self.date or new_context.date

        return self

    def is_complete(self) -> bool:
        return (self.city_name is not None
                and self.date is not None)


class DialogContextStorage:

    def __init__(self, empty_context_factory: Callable[[], DialogContext]):
        self.empty_context_factory = empty_context_factory
        self.user_context = defaultdict(empty_context_factory)

    def get_context(self, user_id, new_context: Optional[DialogContext] = None):
        if new_context is None:
            return self.user_context[user_id]
        return self.user_context[user_id].update(new_context)

    def clear_context(self, user_id):
        self.user_context[user_id] = self.empty_context_factory()
