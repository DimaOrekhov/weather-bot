from abc import ABC, abstractmethod
from src.dialog_context import DialogContext
from src.utils import matches_any, to_separate_word_regex
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

    HELLO_EXPS = tuple(map(
        to_separate_word_regex,
        [
            r"прив(а|(ет?))?", "здравствуй(те)?",
            "hello", "greet(ings)?", r"hi",
            "добрый день", "доброе утро", "добрый вечер"
        ]
    ))

    def accept(self, message) -> bool:
        return matches_any(message.text, GreetingIntent.HELLO_EXPS)


class EndingIntent(Intent):

    BYE_EXPS = tuple(map(
        to_separate_word_regex,
        ["пока", "bye", "good ?bye", "до ?свидания", "ciao"]
    ))

    def accept(self, message) -> bool:
        return matches_any(message.text, EndingIntent.BYE_EXPS)


class WeatherReportIntent(Intent):

    def accept(self, query) -> bool:
        return True
