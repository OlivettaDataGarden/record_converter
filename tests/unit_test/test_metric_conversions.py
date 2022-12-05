"""Module to test the process field class from the record convertor module

"""
from record_converter.mixin_classes.metric_conversions import \
    MetricsCommandsMixin
from record_converter.process import ProcessCommand
from data.test_data_metric_conversions import (
    PARAMS_KNOTS_TO_KM_H, PARAMS_KNOTS_TO_M_S)


class MixinTestClass(ProcessCommand, MetricsCommandsMixin):
    pass


def field_processor(params):
    return MixinTestClass(**params)


def test_convert_knots_to_km_hour():
    """Test if knots are properly converted to km/h
    """
    processor = field_processor(PARAMS_KNOTS_TO_KM_H)
    assert processor.get_value() == 18.53


def test_convert_knots_to_m_per_sec():
    """Test if knots are properly converted to m/s
    """
    processor = field_processor(PARAMS_KNOTS_TO_M_S)
    assert processor.get_value() == 5.14
