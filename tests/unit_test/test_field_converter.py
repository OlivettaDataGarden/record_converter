"""Module to test the field converter class from the record convertor module

"""
from copy import deepcopy
from datetime import date, datetime, timedelta

import pytest

from record_converter.field_converter import RecordFieldConvertor
from data.test_data_field_convertor import (
    BASE_PARAMS, BASE_PARAMS_SELECT_FROM_LIST, BASE_PARAMS_WITH_CONDITION,
    PARAMS_ADD_DATA_FROM_DICT, PARAMS_ADD_KEY_VALUE_FROM_FIELD,
    PARAMS_ADD_KEY_VALUE_FROM_FIELD2, PARAMS_ADD_VALUE_FROM_FIELD,
    PARAMS_ADD_VALUE_FROM_NETSED_FIELD, PARAMS_ALPHA3_TO_ISO3116,
    PARAMS_CHANGE_KEY_NAME, PARAMS_CHANGE_KEY_NAME_NESTED,
    PARAMS_COUNTRY_CODE_FROM_INVALID_PHONE_NUMBER,
    PARAMS_COUNTRY_CODE_FROM_PHONE_NUMBER, PARAMS_DATE_OF_TODAY,
    PARAMS_DAYS_AGO_TO_DATE, PARAMS_DAYS_AGO_TO_DATE_INVALID, PARAMS_DIVIDE_BY,
    PARAMS_DIVIDE_BY_STR, PARAMS_DIVIDE_STR, PARAMS_FIXED_VALUE,
    PARAMS_INSERT_KEY, PARAMS_INVALID_STR_TO_DICT, PARAMS_LIST_TO_DICT,
    PARAMS_MULTIPLY_BY, PARAMS_MULTIPLY_BY_STR, PARAMS_MULTIPLY_STR,
    PARAMS_POST_FIX, PARAMS_PRE_FIX, PARAMS_REMOVE, PARAMS_REMOVE_NESTED_FIELD,
    PARAMS_SELECT_FROM_LIST_VALUE_NOT_FOUND,
    PARAMS_SELECT_FROM_LIST_WITH_NO_LIST,
    PARAMS_SELECT_FROM_LIST_WITH_NON_DICT_ENTRIES, PARAMS_STR_TO_DICT,
    PARAMS_TO_LOWER_STR, PARAMS_TO_STR, PARAMS_TO_UPPER_STR)


def convertor(**params):
    convert_params = deepcopy(BASE_PARAMS)
    convert_params.update(**params)
    return RecordFieldConvertor(**convert_params)


def test_constructor():
    """ test that RecordFieldConvertor can b created """
    url_converter = convertor()
    assert isinstance(url_converter, RecordFieldConvertor)


def test_remove_params_from_url_conversion_1():
    """ test request params are removed from url """
    url_converter = convertor()
    assert url_converter.convert()['url'] == 'www.test.com/'


def test_remove_params_from_url_conversion_2():
    """
    test remove params returns url without also when no url has no params
    """
    url_converter = convertor(**{'record': {'url': 'www.urlwithout.params/'}})
    assert url_converter.convert()['url'] == 'www.urlwithout.params/'


def test_convert_condition_met():
    """ test conversion is exectued when given condition is met """
    url_converter = convertor(**deepcopy(BASE_PARAMS_WITH_CONDITION))
    assert url_converter.convert()['url'] == 'www.test.com/'


def test_convert_condition_not_met():
    """ test is_a_str method evaluates to True with a string as value """
    convertor_params = deepcopy(BASE_PARAMS_WITH_CONDITION)
    convertor_params['conversion_rule']['condition'] = \
        {'equals': 'other str'}
    url_converter = convertor(**convertor_params)
    assert not (url_converter.convert()['url'] == 'www.test.com/')


def test_select_from_list():
    """ test selecting value from list succesfull """
    convert_record = convertor(**deepcopy(BASE_PARAMS_SELECT_FROM_LIST))
    assert convert_record.convert()['list_key_name'] == {
        'item2': 2, 'selector': 2}


def test_select_from_list_when_value_not_found():
    """ test selecting value from list returns none when value not found """
    convert_record = convertor(
        **deepcopy(PARAMS_SELECT_FROM_LIST_VALUE_NOT_FOUND))
    assert convert_record.convert()['list_key_name'] == {}


def test_select_from_list_with_non_dict_entries():
    """ test selecting value from list returns none when value not found """
    convert_record = convertor(
        **deepcopy(PARAMS_SELECT_FROM_LIST_WITH_NON_DICT_ENTRIES))
    assert convert_record.convert()['list_key_name'] == {}


def test_select_from_list_without_a_list():
    """
    test selecting value from list returns none when givem `list` is actually
    not a list
    """
    convert_record = convertor(
        **deepcopy(PARAMS_SELECT_FROM_LIST_WITH_NO_LIST))
    assert convert_record.convert()['list_key_name'] == {}


def test_country_code_from_phone_nunber():
    """
    test selecting value from list returns none when givem `list` is actually
    not a list
    """
    convert_record = convertor(
        **deepcopy(PARAMS_COUNTRY_CODE_FROM_PHONE_NUMBER))
    assert convert_record.convert()['country_code'] == 'NL'


def test_country_code_from_invalid_phone_nunber():
    """
    test selecting value from list returns none when givem `list` is actually
    not a list
    """
    convert_record = convertor(
        **deepcopy(PARAMS_COUNTRY_CODE_FROM_INVALID_PHONE_NUMBER))
    assert convert_record.convert()['country_code'] is None


def test_days_ago_to_date():
    """
    test days ago to date method returning yesterdays date 
    """
    yesterday = datetime.now() - timedelta(1)
    convert_record = convertor(
        **deepcopy(PARAMS_DAYS_AGO_TO_DATE))
    assert convert_record.convert()['days_ago'] == \
        datetime.strftime(yesterday, '%Y-%m-%d')


def test_days_ago_to_date_with_invalid_field():
    """
    test days ago to date method returning none with invalid nr of
    days ago field
    """
    convert_record = convertor(
        **deepcopy(PARAMS_DAYS_AGO_TO_DATE_INVALID))
    assert convert_record.convert()['days_ago'] is None


def test_to_str():
    """
    test to str method turns an int into a strt
    """
    convert_record = convertor(
        **deepcopy(PARAMS_TO_STR))
    assert isinstance(convert_record.convert()['conversion_field'], str)


def test_to_lower_str():
    """
    test to_lower_str method turns str into lowercase
    """
    convert_record = convertor(
        **deepcopy(PARAMS_TO_LOWER_STR))
    assert convert_record.convert()['to_lower'] == 'lowercase'


def test_to_upper_str():
    """
    test to_upper_str method turns str into uppercase
    """
    convert_record = convertor(
        **deepcopy(PARAMS_TO_UPPER_STR))
    assert convert_record.convert()['to_upper'] == 'UPPERCASE'


def test_str_to_dict():
    """
    test str_to_dict returns correct dict
    """
    convert_record = convertor(
        **deepcopy(PARAMS_STR_TO_DICT))
    assert isinstance(convert_record.convert()['to_dict'], dict)
    assert convert_record.convert()['to_dict'] == {"key": "value"}


def test_invalid_str_to_dict():
    """
    test str_to_dict returns empty dict when given invalid input
    """
    convert_record = convertor(
        **deepcopy(PARAMS_INVALID_STR_TO_DICT))
    assert convert_record.convert()['to_dict'] == dict()


def test_add_pre_fix():
    """
    test add_prefix returns string `abc` with prefix `123`
    """
    convert_record = convertor(
        **deepcopy(PARAMS_PRE_FIX))
    assert convert_record.convert()['string'] == "123abc"


def test_add_post_fix():
    """
    test add_postfix returns string `abc` with prefix `def`
    """
    convert_record = convertor(
        **deepcopy(PARAMS_POST_FIX))
    assert convert_record.convert()['string'] == "abcdef"


def test_insert_key():
    """
    test add a field from another field.
    """
    convert_record = convertor(
        **deepcopy(PARAMS_INSERT_KEY))
    assert convert_record.convert()['from_field'] == {'inserted_field': 'abc'}


def test_from_field():
    """
    test add a field from another field.
    """
    convert_record = convertor(
        **deepcopy(PARAMS_ADD_VALUE_FROM_FIELD))
    assert convert_record.convert()['to_field'] == {'nested': 'abc'}


def test_add_data_from_dict():
    """
    test add a antries from a dict to another field
    """
    convert_record = convertor(
        **deepcopy(PARAMS_ADD_DATA_FROM_DICT))
    assert convert_record.convert()['to_field'] == \
        {'1': 1, '2': 2, '0': 0}


def test_add_key_value_from_field():
    """
    test add a field from another field.
    """
    convert_record = convertor(
        **deepcopy(PARAMS_ADD_KEY_VALUE_FROM_FIELD))
    assert convert_record.convert()['to_field'] == {'from_field': 'abc'}


def test_add_key_value_from_field2():
    """
    test add a field from another field.
    """
    convert_record = convertor(
        **deepcopy(PARAMS_ADD_KEY_VALUE_FROM_FIELD2))
    assert convert_record.convert()['to_field'] == \
        {'field2': 'def', 'from_field': 'abc'}


def test_from_nested_field():
    """
    test add a field from another field.
    """
    convert_record = convertor(
        **deepcopy(PARAMS_ADD_VALUE_FROM_NETSED_FIELD))
    assert convert_record.convert()['to_field'] == 'abc'


def test_from_fixed_value():
    """
    test add a field with a fixed value
    """
    convert_record = convertor(
        **deepcopy(PARAMS_FIXED_VALUE))
    assert convert_record.convert()['new_field'] == 'new value'


def test_date_of_today():
    """
    test add a field with date of today
    """
    convert_record = convertor(
        **deepcopy(PARAMS_DATE_OF_TODAY))
    assert convert_record.convert()['today'] == \
        str(date.strftime(date.today(), '%Y-%m-%d'))


def test_change_key_name():
    """
    test changing a field name in the record
    """
    convert_record = convertor(
        **deepcopy(PARAMS_CHANGE_KEY_NAME))
    assert convert_record.convert()['new_name'] == {'nested': 'abc'}
    assert convert_record.convert().get('from_field', None) is None


def test_change_nested_key_name():
    """
    test changing a nested field name in the record
    """
    convert_record = convertor(
        **deepcopy(PARAMS_CHANGE_KEY_NAME_NESTED))
    assert convert_record.convert()['parent_field']['new_nested'] == 'abc'
    assert convert_record.convert()['parent_field'].get(
        'nested', None) is None


def test_list_to_dict():
    """
    test changing list in a field to a dict
    """
    convert_record = convertor(
        **deepcopy(PARAMS_LIST_TO_DICT))
    assert convert_record.convert()['list'] == \
        {'a': 'b', 'c': 'd'}


def test_remove_field():
    """
    test removing a field
    """
    convert_record = convertor(
        **deepcopy(PARAMS_REMOVE))
    assert convert_record.convert().get('removed_field', None) is None


def test_remove_nested_field():
    """
    test removing a field
    """
    convert_record = convertor(
        **deepcopy(PARAMS_REMOVE_NESTED_FIELD))
    assert convert_record.convert()['nested'].get(
        'removed_field', None) is None


def test_convert_cc_alpha_to_iso():
    """
    test conversion of ALPHA 3 country code to iso3116 country code
    """
    convert_record = convertor(
        **deepcopy(PARAMS_ALPHA3_TO_ISO3116))
    assert convert_record.convert()['cc'] == 'FR'


def test_convert_divide_by():
    """
    test conversion dividing a value by a given devider
    """
    convert_record = convertor(
        **deepcopy(PARAMS_DIVIDE_BY))
    assert convert_record.convert()['tx'] == 12.3


def test_convert_divide_by_str():
    """
    test conversion dividing by an str raises an exception
    """
    with pytest.raises(TypeError):
        convert_record = convertor(
            **deepcopy(PARAMS_DIVIDE_BY_STR))
        convert_record.convert()


def test_convert_divide_str():
    """
    test conversion dividing a str returns None
    """
    convert_record = convertor(
        **deepcopy(PARAMS_DIVIDE_STR))
    assert convert_record.convert() == {'tx': None}


def test_convert_mulitply_by():
    """
    test conversion multiply a value by a given multiplier
    """
    convert_record = convertor(
        **deepcopy(PARAMS_MULTIPLY_BY))
    assert convert_record.convert()['tx'] == 12.3


def test_convert_multiply_by_str():
    """
    test conversion multiplying by an str raises an exception
    """
    with pytest.raises(TypeError):
        convert_record = convertor(
            **deepcopy(PARAMS_MULTIPLY_BY_STR))
        convert_record.convert()


def test_convert_multiply_str():
    """
    test conversion multiplying a str returns None
    """
    convert_record = convertor(
        **deepcopy(PARAMS_MULTIPLY_STR))
    assert convert_record.convert() == {'tx': None}
