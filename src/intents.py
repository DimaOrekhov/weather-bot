from abc import ABC, abstractmethod
from src.dialog_context import DialogContext
from typing import Optional


class Intent(ABC):

    def __init__(self, entity_extractor: Optional['EntityExtractor'] = None):
        self.entity_extractor = entity_extractor

    @abstractmethod
    def accept(self, message) -> bool:
        pass

    def to_context(self, query: str, current_context: DialogContext) -> Optional[DialogContext]:
        if self.entity_extractor is None:
            return

        return self.entity_extractor.get_context(query, current_context)


class GreetingIntent(Intent):

    def accept(self, message) -> bool:
        return message.text == "Привет"


class EndingIntent(Intent):

    def accept(self, query) -> bool:
        return query == "Пока"


class WeatherReportIntent(Intent):

    def accept(self, query) -> bool:
        return True
