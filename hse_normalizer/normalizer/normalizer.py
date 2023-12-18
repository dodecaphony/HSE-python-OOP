from dataclasses import dataclass, fields
from hse_normalizer.normalizer.cleaners import Cleaner
from hse_normalizer.normalizer.entities import (
     AddressEntity,
     NumberEntity,
     UserDataEntity,
     DateTimeEntity,
     CustomEntity
)
from natasha import Segmenter, Doc


@dataclass
class EntitiesAggregator:
    address: AddressEntity
    number: NumberEntity
    user_data: UserDataEntity
    date_time: DateTimeEntity


class Normalizer:
    def __init__(self, line: str) -> None:
        self.__text = line
        self.doc = Doc(line)
        self.doc.segment(Segmenter())
        self.tokens = self.doc.tokens
        self.cleaner = Cleaner

    @property
    def text(self) -> str:
        return self.doc.text

    def preprocess(self) -> None:
        cleaner = self.cleaner(self.doc.text)
        self.doc.text = cleaner.initial_cleaning()
        self.doc.text = cleaner.yandex_markings_cleaning()

    def process(self, entity) -> None:
        normalizer = entity(self.doc)
        normalizer.normalize_patterns()
        self.doc.text = normalizer.text

    def postprocess(self, entity) -> None:
        normalizer = entity(self.doc)
        normalizer.normalize_patterns()
        self.doc.text = normalizer.text
        self.doc.text = self.cleaner(self.doc.text).final_cleaning()

    def normalize(self) -> None:
        self.preprocess()
        self.doc.tokens = Normalizer(self.text).tokens
        [self.process(ent.type) for ent in fields(EntitiesAggregator)]
        self.postprocess(CustomEntity)
