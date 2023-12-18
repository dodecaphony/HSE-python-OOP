import pytest
import hse_normalizer.normalizer.normalizer as norm

from dataclasses import fields
from samples import (
    address_samples,
    personal_samples,
    latin_samples,
    measure_samples,
    decimal_samples,
    time_samples,
    date_samples,
    ordinal_samples
)


class __TestAggregator(norm.EntitiesAggregator):
    address = fields(norm.EntitiesAggregator)[0].type
    number = fields(norm.EntitiesAggregator)[1].type
    user_data = fields(norm.EntitiesAggregator)[2].type
    date_time = fields(norm.EntitiesAggregator)[3].type


def __processing(samples, entity, intermediate=False):
    for sample in samples:
        normalizer = norm.Normalizer(sample)
        normalizer.preprocess()
        normalizer.process(entity)
        if intermediate:
            normalizer.postprocess(norm.CustomEntity)
        assert normalizer.text == samples[sample]


def __postprocessing(samples):
    for sample in samples:
        normalizer = norm.Normalizer(sample)
        normalizer.postprocess(norm.CustomEntity)
        assert normalizer.text == samples[sample]


def test_address_processing():
    __processing(address_samples, __TestAggregator.address)


def test_ordinal_processing():
    __processing(ordinal_samples, __TestAggregator.number)


def test_decimal_processing():
    __processing(decimal_samples, __TestAggregator.number)


def test_measure_processing():
    __processing(measure_samples, __TestAggregator.number)


def test_date_processing():
    __processing(date_samples, __TestAggregator.date_time)


def test_time_processing():
    __processing(time_samples, __TestAggregator.date_time)


def test_user_data_processing():
    __processing(personal_samples, __TestAggregator.user_data, intermediate=True)


def test_latin_processing():
    __postprocessing(latin_samples)
