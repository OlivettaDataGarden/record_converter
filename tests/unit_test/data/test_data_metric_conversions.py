"""
Module to provide test data for unit tests for metric_conversions
mixin class of record_converter module

"""
from record_converter.converter import ConvertRecord

PARAMS_KNOTS_TO_KM_H = {
    'record': {'field1': 10},
    'record_convertor': ConvertRecord,
    'process_command': '$knots_to_km_per_hour',
    'process_args': 'field1',
}

PARAMS_KNOTS_TO_M_S = {
    'record': {'field1': 10},
    'record_convertor': ConvertRecord,
    'process_command': '$knots_to_meter_per_second',
    'process_args': 'field1',
}
