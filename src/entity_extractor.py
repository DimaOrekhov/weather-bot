from abc import ABC, abstractmethod
from typing import List, Iterable
import re

from src.dialog_context import DialogContext
from src.utils import to_full_match_regex


SAINT_PETERSBURG = "Saint Petersburg"
MOSCOW = "Moscow"
RU = "RU"


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
        date = "ceгодня"
        current_context.date = date
        return current_context


class NatashaLocationExtractor(EntityExtractor):

    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        city_name = None
        state_code = RU
        current_context.city_name = city_name
        current_context.state_code = state_code
        return current_context


class HandcraftedLocationExtractor(EntityExtractor):

    SAINT_PETERSBURG_ALIASES = tuple(map(
        to_full_match_regex,
        [r"спб",
         r"питере?",
         r"петербурге?",
         r"spb",
         r"saint[-\s]petersburg"]
    ))
    MOSCOW_ALIASES = tuple(map(
        to_full_match_regex,
        [r"мск",
         r"москва",
         r"msk",
         r"moscow"]
    ))

    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        city_name = None
        state_code = None
        if HandcraftedLocationExtractor.is_alias_of(
                query, HandcraftedLocationExtractor.SAINT_PETERSBURG_ALIASES
        ):
            city_name = SAINT_PETERSBURG
            state_code = RU
        elif HandcraftedLocationExtractor.is_alias_of(
                query, HandcraftedLocationExtractor.MOSCOW_ALIASES
        ):
            city_name = MOSCOW
            state_code = RU

        current_context.city_name = city_name
        current_context.state_code = state_code
        return current_context

    @staticmethod
    def is_alias_of(query: str, aliases: Iterable[re.Pattern]):
        return any(regex.fullmatch(query) is not None for regex in aliases)


class SequentialEntityExtractor(EntityExtractor):

    def __init__(self, extractors: List[EntityExtractor]):
        self.extractors = extractors

    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        for extractor in self.extractors:
            if current_context.is_complete():
                break

            current_context = extractor.get_context(query, current_context)
        return current_context
