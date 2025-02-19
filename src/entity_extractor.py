from abc import ABC, abstractmethod
from typing import List
from natasha import (
    Doc,
    NewsNERTagger,
    NewsEmbedding,
    DatesExtractor,
    Segmenter,
    MorphVocab
)
import datetime

from src.dialog_context import DialogContext
from src.utils import to_full_match_regex, full_matches_any, or_else, to_separate_word_regex


SAINT_PETERSBURG = "Saint Petersburg"
MOSCOW = "Moscow"
RU = "RU"


class EntityExtractor(ABC):

    @abstractmethod
    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        pass


class NatashaDateExtractor(EntityExtractor):

    DATES_EXTRACTOR = DatesExtractor(MorphVocab())

    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        date = None
        extracted = list(self.DATES_EXTRACTOR(query))
        if extracted:
            date = self.get_relative_date(extracted[0].fact)
        current_context.date = date
        return current_context

    @staticmethod
    def get_relative_date(date):
        today = datetime.datetime.now()  # TODO: Add time zone!
        year = or_else(date.year, today.year)
        month = or_else(date.month, today.month)
        day = or_else(date.day, today.day)
        delta = datetime.datetime.combine(
            date=datetime.date(year, month, day),
            time=today.time()
        ) - today
        return delta.days


class HandcraftedDateExtractor(EntityExtractor):

    TODAY_ALIASES = tuple(map(
        to_full_match_regex,
        [r"сегодня?",
         r"сейчас",
         r"щас?"]
    ))
    TOMORROW_ALIASES = tuple(map(
        to_full_match_regex,
        [r"завтра?"]
    ))
    AFTER_TOMORROW_ALIASES = tuple(map(
        to_full_match_regex,
        [r"после ?завтра"]
    ))

    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        date = current_context.date

        if full_matches_any(query, HandcraftedDateExtractor.TODAY_ALIASES):
            date = 0
        elif full_matches_any(query, HandcraftedDateExtractor.TOMORROW_ALIASES):
            date = 1
        elif full_matches_any(query, HandcraftedDateExtractor.AFTER_TOMORROW_ALIASES):
            date = 2

        current_context.date = or_else(current_context.date, date)
        return current_context


class NatashaLocationExtractor(EntityExtractor):

    SEGMENTER = Segmenter()
    TAGGER = NewsNERTagger(NewsEmbedding())

    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        city_name = self.get_loc(query) or self.get_loc(query, capitalize=True)
        if city_name is not None:
            city_name = self.to_known_loc(city_name)
        state_code = RU
        current_context.city_name = city_name
        current_context.state_code = state_code
        return current_context

    @staticmethod
    def to_known_loc(loc: str):
        if 'санкт-петербург' in loc.lower() \
                or 'санкт петербург' in loc.lower() \
                or "спб" in loc.lower() \
                or "питер" in loc.lower() \
                or "петербург" in loc.lower():
            return SAINT_PETERSBURG
        if 'москв' in loc.lower() \
                or 'москов' in loc.lower()\
                or 'мск' in loc.lower():
            return MOSCOW
        return loc

    @classmethod
    def get_loc(cls, query: str, capitalize: bool = False):
        doc = Doc(query)
        doc.segment(cls.SEGMENTER)
        if capitalize:
            capitalized_text = " ".join(
                tok.text.capitalize() for tok in doc.tokens
            )

            doc = Doc(capitalized_text)
            doc.segment(cls.SEGMENTER)
        doc.tag_ner(cls.TAGGER)
        for span in doc.ner.spans:
            if span.type == 'LOC':
                index = slice(span.start, span.stop)
                return capitalized_text[index] if capitalize else query[index]


class HandcraftedLocationExtractor(EntityExtractor):

    SAINT_PETERSBURG_ALIASES = tuple(map(
        to_full_match_regex,
        [r"спб",
         r"питер[еа]?",
         r"петербург[еа]?",
         r"spb",
         r"saint[-\s]petersburg"]
    ))
    MOSCOW_ALIASES = tuple(map(
        to_full_match_regex,
        [r"мск",
         r"москв[аеы]?",
         r"msk",
         r"moscow"]
    ))

    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        city_name = None
        state_code = None
        if full_matches_any(query, HandcraftedLocationExtractor.SAINT_PETERSBURG_ALIASES):
            city_name = SAINT_PETERSBURG
            state_code = RU
        elif full_matches_any(query, HandcraftedLocationExtractor.MOSCOW_ALIASES):
            city_name = MOSCOW
            state_code = RU

        current_context.city_name = or_else(current_context.city_name, city_name)
        current_context.state_code = or_else(current_context.state_code, state_code)
        return current_context


class SequentialEntityExtractor(EntityExtractor):

    def __init__(self, extractors: List[EntityExtractor]):
        self.extractors = extractors

    def get_context(self, query: str, current_context: DialogContext) -> DialogContext:
        for extractor in self.extractors:
            if current_context.is_complete():
                break

            current_context = extractor.get_context(query, current_context)
        return current_context
