"""Module to test the field converter class from the record convertor module

"""
from record_converter.date_converter import DateFieldConvertor
from data.test_data_date_convertor import (
    BASE_PARAMS, BASE_PARAMS_DOTTED, BASE_PARAMS_NESTED_DATE_FIELD,
    BASE_PARAMS_NONE_DATE, BASE_PARAMS_UNIX_DT_STAMP, BASE_PARAMS_YYYY_MM_DD,
    BASE_PARAMS_YYYY_MM_DD_Time, BASE_PARAMS_YYYY_MM_DD_UNDERSCORE)


def date_convertor(params):
    return DateFieldConvertor(**params)


def test_constructor():
    """ test that RecordFieldConvertor can b created """
    convertor = date_convertor(BASE_PARAMS)
    assert isinstance(convertor, DateFieldConvertor)


def test_convert_yyyy_mm_dd():
    """ test conversion from YYYY_DD_MM to YYYY_MM_DD success """
    convertor = date_convertor(BASE_PARAMS_YYYY_MM_DD)
    assert convertor.convert_date()['date'] == '2021-02-21'


def test_convert_dd_mm_yyyy():
    """ test conversion from DD_MM_YYYY to YYYY_MM_DD success """
    convertor = date_convertor(BASE_PARAMS)
    assert convertor.convert_date()['date'] == '2021-02-21'


def test_convert_dd_mm_yyyy_dotted():
    """ test conversion from DD.MM.YYYY to YYYY_MM_DD success """
    convertor = date_convertor(BASE_PARAMS_DOTTED)
    assert convertor.convert_date()['date'] == '2021-02-21'


def test_nested_convert_dd_mm_yyyy():
    """ test conversion from DD_MM_YYYY to YYYY_MM_DD success """
    convertor = date_convertor(BASE_PARAMS_NESTED_DATE_FIELD)
    assert convertor.convert_date()['date']['nested_date'] == '2021-02-21'


def test_convert_yyyy_mm_dd():
    """ test conversion from YYYY_MM_DD to YYYY_MM_DD success """
    convertor = date_convertor(BASE_PARAMS_YYYY_MM_DD)
    assert convertor.convert_date()['date'] == '2021-02-21'


def test_convert_yyyy_mm_dd_underscore():
    """ test conversion from YYYY_MM_DD to YYYY_MM_DD success """
    convertor = date_convertor(BASE_PARAMS_YYYY_MM_DD_UNDERSCORE)
    assert convertor.convert_date()['date'] == '2021-02-21'


def test_convert_yyyy_mm_dd_time():
    """ test conversion from YYYY_MM_DD:Time to YYYY_MM_DD success """
    convertor = date_convertor(BASE_PARAMS_YYYY_MM_DD_Time)
    assert convertor.convert_date()['date'] == '2021-02-21'


def test_convert_unix_date_time_stamp():
    """ test conversion from YYYY_MM_DD:Time to YYYY_MM_DD success """
    convertor = date_convertor(BASE_PARAMS_UNIX_DT_STAMP)
    assert convertor.convert_date()['date'] == '2021-02-21'


def test_convert_no_date_field():
    """ test conversion where input field is None also returns None """
    convertor = date_convertor(BASE_PARAMS_NONE_DATE)
    assert convertor.convert_date()['date'] is None
