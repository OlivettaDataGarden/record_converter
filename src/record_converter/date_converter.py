"""Module to provide DateFieldConvertor class.

This class allows you to do a number of date conversions on a record. This is
usually done prior to creating a new record from this existing record, thus
ensuring a well formatted record prior to processing.

Conditions can be included and conversions will only be executed if all
conditions comply.

Generic format in the rules_dict:
{ 
    'date_field': <name of date field that needs to be converted>,
    'conditions: {<condition name> : <condition value when needed>},
    'format': <format name that is used in date_field>
}

Availale date formats (from which to convert to YYYY-MM-DD)
    - DD-MM-YYYY
    - DD.MM.YYYY
    - YYYY_MM_DD
    - YYYY_MM_DD:Time
    - UNIX_DT_STAMP
    - YYYY-MM-DD
"""
from datetime import datetime
from typing import Dict

import jmespath

from record_converter.evaluate_condition import Conditions

CONV_METHODS: Dict[str, str] = {
    "DD-MM-YYYY": 'day_month_year',
    "DD.MM.YYYY": 'day_month_year_dotted',
    "YYYY_MM_DD": 'year_month_day',
    "YYYY_MM_DD:Time": 'year_month_day_time',
    "UNIX_DT_STAMP": 'unix_dt_stamp',
    "YYYY-MM-DD": 'year_month_date'
}


class DateFieldConvertor():
    """
    Class to perform conversions on a given record and return the updated
    record

    args:
        record (dict): record that needs some conversion action
        conversion_rule (dict) :
            instructions about the conversion. Should at least have
                - fieldname -> which field will be converted
                - actions -> list of actions to be applied
                - conditions (optional) -> conditions required to
                                           run the conversion

    returns:
        record (dict): converted record
    """

    def __init__(self, record: Dict, conversion_rule: Dict[str, str]):
        self.record = record
        self.conversion_rule = conversion_rule
        self.date_field_key_name = self._get_date_field_key_name()

    @staticmethod
    def unix_dt_stamp(unix_dt_stamp: str) -> str:
        """convert Unix date time stamp to YYYY-MM-DD"""
        datetime_date = datetime.fromtimestamp(int(unix_dt_stamp))
        return datetime_date.strftime("%Y-%m-%d")

    @staticmethod
    def year_month_date(date_str: str) -> str:
        """convert YYYY-MM-DD to YYYY-MM-DD"""
        return date_str

    @staticmethod
    def year_month_day_time(date_str: str) -> str:
        """convert YYYY-MM-DD:time to YYYY-MM-DD"""
        return date_str[0:10]

    @staticmethod
    def year_month_day(date_str: str) -> str:
        """convert YYYY-MM-DD to YYYY-MM-DD"""
        datetime_date = datetime.strptime(date_str, '%Y_%m_%d')
        return datetime_date.strftime("%Y-%m-%d")

    @staticmethod
    def day_month_year(date_str: str) -> str:
        """convert DD-MM-YYYY to YYYY-MM-DD"""
        datetime_date = datetime.strptime(date_str, '%d-%m-%Y')
        return datetime_date.strftime("%Y-%m-%d")

    @staticmethod
    def day_month_year_dotted(date_str: str) -> str:
        """convert DD.MM.YYYY to YYYY-MM-DD"""
        datetime_date = datetime.strptime(date_str, '%d.%m.%Y')
        return datetime_date.strftime("%Y-%m-%d")

    def convert_date(self) -> Dict:
        """
        Method to convert a date field in a record into into a
        'YYYY-MM-DD' string date format.
        """
        date_formatter = CONV_METHODS.get(
                self.conversion_rule.get('format', ''), '')
        if not date_formatter:
            raise NotImplementedError(
                f'Format date convertor {date_formatter}')
        date_field_value = self._get_field()

        if date_field_value and self.all_conditions_true(date_field_value):
            date_in_new_format = getattr(
                self, date_formatter)(date_field_value)
            self.update_field_with_date(date_in_new_format)

        return self.record

    def all_conditions_true(self, date_field_value: str) -> bool:
        """Returns True if all provided conditions are satisfied.
        """
        conditions = self.conversion_rule.get('condition', False)
        if not conditions:
            return True

        return Conditions(
            provided_conditions=conditions,
            value=date_field_value).evaluate()

    def update_field_with_date(self, date_in_new_format: str) -> None:
        """
        updates the datefield in the record to date_in_new_format

        args:
            - date_in_new_format (str)
        """
        nested_field_names = self.date_field_key_name.split('.')
        first_field_name = nested_field_names.pop(0)
        # if it is not a nested field update first level field name and return
        if not nested_field_names:
            self.record.update({first_field_name: date_in_new_format})
            return

        # if it is a nested field capture the fieldname that needs to be
        # updated (i.e. the last field name in thel list).
        last_field = nested_field_names.pop()

        # find the nested dict in whih the last_field is a (nested) key
        field_value = self.record.get(first_field_name, None)
        if field_value is None:
            return None

        # with the list of nested field name we dig deeper into the
        # structure to get to the dict containing the last field name
        for field_name in nested_field_names:
            field_value = field_value.get(field_name, {})

        # update that value of `last_field` in that dict
        if field_value is not None:
            field_value.update({last_field: date_in_new_format})


    def _get_date_field_key_name(self):
        # initially used '__' as key seperator but migrating to using
        # `.` as seperator. This line to allow old conversion yaml files
        # not to fail
        date_field_in_record = self.conversion_rule.get('date_field')
        date_field_in_record.replace('__', '.')
        return date_field_in_record

    def _get_field(self) -> str:
        """
        returns a value from a nested field in the record.
        nested field names should be seperated by `__`

        if value is not found or can not be converted into a string an empty
        string is returned
        """
        # key elemenets in nested keys are surround with "". For exmample
        # key.example-1 becomes "key"."example-1".
        # Needed for jmespath can hande special characters in the keys
        nested_field_names = self.date_field_key_name.split('.')
        nested_key = \
            '.'.join(['"' + name + '"' for name in nested_field_names])
        try:
            date_value_from_record = jmespath.search(nested_key, self.record)
        except jmespath.exceptions.ParseError:
            return ''

        return str(date_value_from_record) if date_value_from_record else ''