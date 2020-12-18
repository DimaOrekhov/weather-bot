from abc import ABC, abstractmethod
from typing import List

from src.dialog_context import DialogContext


class EntityExtractor(ABC):

    @abstractmethod
    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        pass


class NatashaDateExtractor(EntityExtractor):

    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        date = None
        current_context.date = date
        return current_context


class HandcraftedDateExtractor(EntityExtractor):

    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        date = None
        current_context.date = date
        return current_context


class NatashaLocationExtractor(EntityExtractor):

    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        city_name = None
        state_code = None
        current_context.city_name = city_name
        current_context.state_code = state_code
        return current_context


class HandcraftedLocationExtractor(EntityExtractor):

    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        pass


class SequentialEntityExtractor(EntityExtractor):

    def __init__(self, extractors: List[EntityExtractor]):
        self.extractors = extractors

    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        for extractor in self.extractors:
            if current_context.is_complete():
                break

            current_context = extractor.get_context(query, current_context)
        return current_context
