"""Module to test the ConvertRecord class from the record convertor module

"""
from copy import deepcopy

import pytest

from record_converter.converter import ConvertRecord
from data import test_data_convertor as tdc


def get_convertor(params):
    copy_of_params = deepcopy(params)
    expected_results = copy_of_params.pop('expected_results', None)
    return ConvertRecord(**copy_of_params), expected_results

def test_convert_record_exists():
    assert ConvertRecord


def test_constructor():
    """ test that ConvertRecord can be created """
    convertor, _ = get_convertor(tdc.BASE_PARAMS)
    assert isinstance(convertor, ConvertRecord)


def test_base_conversion():
    """ test a base conversion """
    convertor, expected_results = get_convertor(tdc.BASE_PARAMS)
    assert convertor.convert() == expected_results


def test_dict_rule():
    """ test a conversion with a dict in a dict """
    convertor, expected_results = get_convertor(tdc.PARAMS_DICT_RULE)
    assert convertor.convert() == expected_results


def test_allow_explicit_set_to_none_value():
    """
    test a conversion to return a field with None when set_to_non_value is used
    """
    convertor, expected_results = get_convertor(
        tdc.PARAMS_ALLOW_NONE_VALUE_NONE)
    assert convertor.convert() == expected_results


def test_allow_none_value_with_none():
    """ test a conversion with a dict in a dict """
    convertor, expected_results = get_convertor(
        tdc.PARAMS_RETURN_EXPLICIT_NONE_VALUE_SET_TO_NON)
    assert convertor.convert() == expected_results


def test_allow_none_value_with_value():
    """ test a conversion with a dict in a dict """
    convertor, expected_results = get_convertor(
        tdc.PARAMS_ALLOW_NONE_VALUE_WITH_VALUE)
    assert convertor.convert() == expected_results


def test_skip_true():
    """ test record skipped because given condition is True """
    convertor, expected_results = get_convertor(tdc.PARAMS_SKIP_TRUE)
    assert convertor.convert() == expected_results


def test_skip_false():
    """ test record not skipped because given condition is False """
    convertor, expected_results = get_convertor(tdc.PARAMS_SKIP_FALSE)
    assert convertor.convert() == expected_results


def test_skip_with_invalid_params():
    """ test record convert raise exception for invalid skip params """
    convertor, _ = get_convertor(tdc.PARAMS_SKIP_INVALID)
    with pytest.raises(ValueError):
        convertor.convert()


def test_process_command():
    """ test record convert process a command properly"""
    convertor, expected_results = get_convertor(tdc.PARAMS_PROCESS_COMMAND)
    assert convertor.convert() == expected_results


def test_convert_record():
    """ test record convert converts values in the record with $convert command
    """
    convertor, expected_results = get_convertor(tdc.PARAMS_CONVERT)
    assert convertor.convert() == expected_results


def test_convert_date_in_record():
    """
    test record convert converts a date in the record with $convert_date
    command
    """
    convertor, expected_results = get_convertor(tdc.PARAMS_DATE_CONVERT)
    assert convertor.convert() == expected_results


def test_data_class_not_defined():
    """
    test record convert raise exception when non defined dataclass is used
    """
    convertor, _ = get_convertor(tdc.PARAMS_DATA_CLASS_NOT_DEFINED)
    with pytest.raises(ValueError):
        convertor.convert()


def test_data_class():
    """
    test record convert with dataclass success
    """
    convertor, expected_results = get_convertor(tdc.PARAMS_DATA_CLASS)
    assert convertor.convert() == expected_results


def test_data_class_with_method():
    """
    test record convert with dataclass and method success 
    """
    convertor, expected_results = get_convertor(
        tdc.PARAMS_DATA_CLASS_WITH_METHOD)
    assert convertor.convert() == expected_results


def test_converter_returns_none():
    """
    test that if a convertor command returns a none value for a field name that
    this field name is not included in the result
    """
    convertor, expected_results = get_convertor(
        tdc.PARAMS_RETURN_NONE_FROM_COMMAND)
    assert convertor.convert() == expected_results


def test_command_in_root():
    """
    test that a command in root returns the expected results.
    Ensure that root commands do not overwrite other root fields
    """
    convertor, expected_results = get_convertor(
        tdc.PARAMS_COMMAND_IN_ROOT)
    assert convertor.convert() == expected_results


def test_nested_fields():
    """
    test that correct values are return for nested field arguments
    """
    convertor, expected_results = get_convertor(
        tdc.PARAMS_NESTED_FIELD)
    assert convertor.convert() == expected_results


def test_nested_fields_with_special_char():
    """
    test that correct values are return for nested field arguments
    with special chars !, # and -
    """
    convertor, expected_results = get_convertor(
        tdc.PARAMS_NESTED_FIELD_WITH_SPECIAL_CHAR)
    assert convertor.convert() == expected_results
