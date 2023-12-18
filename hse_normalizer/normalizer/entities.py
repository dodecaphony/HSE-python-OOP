import natasha
import re

from .interfaces import interfaces
from .patterns import (
     address_patterns,
     number_patterns,
     other_patterns,
     date_time_patterns,
     user_data_patterns
)
from .sets import PREVS


class NormalizerStrategy:
    def __init__(self, patterns):
        self.patterns = patterns

    def normalize(self, text, tokens):
        for pt in self.patterns:
            text = re.sub(pt.pattern, lambda match: self.__replace_token(match, pt, tokens), text)
        return text

    def __replace_token(self, match, pt, tokens):
        token_to_replace = match.group(0)
        replacement = interfaces.get(pt.name)(
            token_to_replace,
            match.groupdict(),
            self.__get_case(match, tokens),
            pt.lemma)
        return replacement

    @staticmethod
    def __get_case(match, tokens):
        prev_token = None
        for token in tokens:
            if token.start == match.start() and prev_token:
                return PREVS.get(prev_token.text)
            prev_token = token


class Entity:
    def __init__(self, doc: natasha.Doc, strategy: NormalizerStrategy) -> None:
        self.__doc = doc
        self.__text = self.__doc.text
        self.__tokens = self.__doc.tokens

        self.strategy = strategy

    @property
    def text(self) -> str:
        return self.__text

    @text.setter
    def text(self, changes) -> None:
        self.__text = changes

    @property
    def tokens(self):
        return self.__tokens

    def normalize_patterns(self) -> None:
        self.__text = self.strategy.normalize(self.__text, self.__tokens)


class AddressEntity(Entity):
    def __init__(self, doc) -> None:
        super().__init__(doc, NormalizerStrategy(address_patterns))


class NumberEntity(Entity):
    def __init__(self, doc) -> None:
        super().__init__(doc, NormalizerStrategy(number_patterns))


class UserDataEntity(Entity):
    def __init__(self, doc) -> None:
        super().__init__(doc, NormalizerStrategy(user_data_patterns))


class DateTimeEntity(Entity):
    def __init__(self, doc) -> None:
        super().__init__(doc, NormalizerStrategy(date_time_patterns))


class CustomEntity(Entity):
    def __init__(self, doc) -> None:
        super().__init__(doc, NormalizerStrategy(other_patterns))
