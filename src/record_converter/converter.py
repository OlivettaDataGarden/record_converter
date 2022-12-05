"""
Module to define record conversion functionality.

Classes:
    - RecordConverter: Public class to be used to convert records based upon
                       conversion definition in YAML file
    - ConvertRecord: Helper class that actually does convert the records

"""
from dataclasses import asdict
from typing import Dict, Optional

import jmespath

from record_converter.date_converter import DateFieldConvertor
from record_converter.evaluate_condition import Conditions
from record_converter.field_converter import RecordFieldConvertor
from record_converter.helper.dict_helper import dict_without_non_values
from record_converter.process import ProcessCommand
from record_converter.settings import DataClass


COMMANDS_TO_ALLOW_A_NONE_RESULT = [
    '$set_to_none_value', '$allow_none_value'
]


class ConvertRecord():
    """
    Helper to convert a record into a data stucture (dict) that is required
    based upon a rules set defined by the rules dict.

    args:
        - record (dict) : record that needs to be converted
        - rules (dict) : rules set for converting the record
        - data_classes (dict, optional) :
            dict with name of dataclass and dataclass object as key value.
            These dataclasses can be used in the rules dict to validate the
            generated data structure against the dataclass and use dataclass
            method to do additional data validation / creation
        - command_class (ProcessCommand) :
            Class that handles all the commands provided in the rules dict to
            generate data from the data in the records while creating the new
            data structure
            A Subclassed version of ProcessCommand allows to extend the list of
            available commands and can be used by ConvertRecord via this
            argument. By default this arg is set to None in which case the
            ProcessCommand class itself is used to interpret commands
        - convertor_class
            Class to handle conversions in the input record. Defaults to
            RecordFieldConvertor and when subclassed can be used via this
            argument.
        - date_coverter_class (DateFieldConvertor):
            Class to handle date conversions in the input record. Defaults to
            DateFieldConvertor and when subclassed can be used via this
            argument.
        - skip response (any type):
            Response to be returned when a conversion is not done due to a skip
            rule

    public methods:
        - convert : returns the data structure from the converted record

    The Rules dict defines key names and values which are used to generate the
    required data structure. The key names are processed from top of dict to
    bottom. So it is import to have the right order of keys and commands.

    The dict should be set up with following rules in mind.

    1. regular key (string) not starting with a `$`
        -> this will create a key in the output data dict with content that
           depends on the given value of the key
            a. if the given value in rules dict is a string then this value
               will be used as a lookup key to retrieve a value from the input
               record. This lookup key can be netsed. In that case the nesting
               needs to be seperated by a `.`
               i.e. rules dict {'car': 'car_name' } with input record
               example_rec will result in {'car': <example_rec['car_name']>}
            b. if the given value in rules dict is a dict then this dict will
               be itself evaluated by ConvertRecord. The result of this
               evaluation will be returned as value for the initial key.
               i.e. input dict {'car': {'brand': 'car_name'} } with input
               record example_rec will result in
               {'car': {'brand': <example_rec['car_name']>}

    2. keys in input dict starting with a $ sign will be evaluated as a
       command by command_class. The following commands are available from
       default in the ProcessCommand:
        $fixded_value, $split_field, $int_from_string, $join,
        $normalized_address, $point, $full_record, $join_key_value, $from_list,
        $to_list, $to_int

       there are two special $commands

       a. $convert
            This command allows you to make changes to the input record prior
            to converting it to the required data dict. $
            subfields:
                - fieldname -> fieldname in input record that needs change
                - actions -> list with actions to be executed on the field
                             value. Possible actions defined as key value pairs
                             in actions list
                    a. add_value_from_field: from_field name (str)
                        replaces the field name in scope with the value
                        input_record[from_field name]
                    b. add_prefix: value (str)
                        adds the given value to the beginning of the fieldname
                        value
                    c. add_postfix: value (str)
                        adds the given value to the end of the fieldname value
                    d. fixed_value (str): sets a fixed value to the field
                    d. change_key_name_to (str)
                    e. remove (bool)
                - condition -> condition that needs to be met for the
                               conversion to be exectuded. Field is optional.
                               If not provided conversion will be executed.
                               possible conditions
                               str_length: value(int)
                                    conversion executed when length of given
                                    field is equal to given value
                               is_null: value (true or false)
                                    conversion executed when given field value
                                    is or is not None (depending) on confition
                                    value

        b. $join :
            takes a list of keys as input and joins the values retrieved from
            the input record with these keys. Special keys are
                $seperatorX - add seperator to the join using X as seperator
                $XYZ        - adds a fixed value to the seperator
        b. $fixed_value :
            returns the value provided with this command and returns it as a
            string
        c. $get_coordinates :
            retrieves geojson point object based upon provide address detail.
            Address details are retrieved from input record using fields
            `zip_code_key`, `city_name_key`, 'address_keys`. Also
            `country_code` with a fixed value for the iso3116_country_code
             needs to be provided
        d. $format_date:
            ensure that date fields are in a single str format (YYYY-MM-DD).
            Required input is:
                - `date_field`
                    indicating the field in scope, i.e. the field
                    that holds the date to be converted
                - `format` field
                    indiating the date format used in the input
                    formats that can be converted
                        - YYYY-MM-DD
                        - DD-MM-YYYY
                        - UNIX_DT_STAMP
        e. $point:
            create GeoJOSN point field. Required input fields are:
                - lat: contains lattitude field name in record
                - lon: contains longitude field name in record
        f. $skip:
            skips entire record and returns nonne as result
        g. $to_list:
            adds multiple values to a list. Should be accompanied with a list
            of source record fieldnames
        h. $from_list:
            converst a list of similar object in source record to a list with
            similar objects in target record.
            Must inlcude field `list_field_name` to define the list in the
            source record.
            all other field names will used to generate the object for the
            target record. BE AWARE reference to fields in the source record
            list object must be relative to the lsit object and not to the
            source record. This is because the list objects can only be
            proceessed indepently from the overall source record.
        i. $to_price
            removes currency (by default EUR) and returns amount in int
    """

    def __init__(
            self,
            rules: Dict,
            record: Dict,
            data_classes: Dict[str, DataClass],
            command_class=None,
            date_coverter_class=None,
            convertor_class=None,
            skip_response=None):
        self.rules = rules
        self.record = record
        self.data_classes = data_classes
        self.command_class = command_class or ProcessCommand
        self.date_coverter_class = date_coverter_class or DateFieldConvertor
        self.convertor_class = convertor_class or RecordFieldConvertor
        self.skip_response = skip_response

    def convert(self):
        """
        Method to covert the provided record accoring to the given rules
        """
        result = {}
        if not self.rules:
            return
        for key, value in self.rules.items():
            if '$skip' in key:
                provided_condition = value.get('condition')
                fieldname = value.get('fieldname')
                if not (provided_condition and fieldname):
                    raise ValueError(
                        'Missing fieldname and/or condition for $skip command')

                field_value = self._get_field(fieldname)

                # if condition is met the record should be skipped and None
                # should be returned
                if Conditions(provided_condition, field_value).evaluate():
                    return self.skip_response
                # if condition is not met continue to the next rule
                continue

            if '$add_convertor' in key:
                """Adds a convertor command to the record.
                This method can be used to created a conversion record from a template conversion record.
                """
                fieldname = value.get('fieldname')
                action_type = value.get('action_type')
                action_value = value.get('action_value')
                convertor_name = "$convert_" + fieldname
                convertor = {
                    'fieldname': fieldname,
                    'actions': [{
                        action_type: self._get_field(action_value)
                    }
                    ]
                }
                self.record.update(
                    {convertor_name: convertor})
                continue

            if '$add_many_values' in key:
                """update a list of nested keys with a value for the record."""
                for field_name_key, field_name in value.items():
                    conversion_rule = {
                        'fieldname': field_name_key,
                        'actions': [{'add_value_from_field': field_name}]
                    }
                    self.record = self.convertor_class(
                        record=self.record,
                        conversion_rule=conversion_rule).convert()
                continue

            if '$convert' in key:
                self.record = self.convertor_class(
                    record=self.record, conversion_rule=value).convert()
                continue

            if '$format_date' in key:
                self.record = self.date_coverter_class(
                    record=self.record, conversion_rule=value).convert_date()
                continue

            if key == '$data_class':
                try:
                    return self._data_class(value.copy())
                except TypeError:
                    return None

            if key[0] == '$':
                conversion = self.command_class(
                    record=self.record, process_command=key,
                    process_args=value,
                    record_convertor=self.convert_record).get_value()

                if isinstance(conversion, dict):
                    result.update(conversion)
                    return result

                return conversion

            if isinstance(value, dict):
                dict_result = self.convert_record(
                    rules=value, record=self.record).convert()
                if self._command_allows_none_result(value):
                    result[key] = None
                if dict_result:
                    result[key] = dict_result
                continue

            if isinstance(value, str):
                # setup with None needed to allow result_for_key to be 0
                result_for_key = self._get_field(value)
                if result_for_key is not None:
                    result[key] = result_for_key
                continue

            raise ValueError(f'could not resolve key `{key}`')

        return result

    def _command_allows_none_result(self, value):
        """
        Checks if a command is allowed to return a non value in the resulting
        record.
        If False is returned a field with a None value will not be resturned in
        the result dict

        Args:
            value (str): the command in scope

        Returns:
            Bool: Returns True if command can result in None value in record
        """
        return any([
            (command in value) for command in
            COMMANDS_TO_ALLOW_A_NONE_RESULT
        ])

    def _data_class(self, data_class_params):

        data_class_name = data_class_params.pop('data_class_name', False)
        data_class = self.data_classes.get(data_class_name, False)
        if not data_class:
            raise ValueError(f'no dataclass found for {data_class_name}')
        params = data_class_params.pop('params', {})
        methods = data_class_params.pop('methods', [])
        data_class_data = self.convert_record(
            rules=params, record=self.record).convert() or {}
        data_class_obj = data_class(**data_class_data)
        data_class_obj = \
            self._run_methods_on_a_dataclass(data_class_obj, methods)
        if data_class_params.get('keep_non_values'):
            return data_class_obj

        return dict_without_non_values(data_class_obj)

    def _run_methods_on_a_dataclass(self, data_class_obj, methods):
        for method in methods:
            [[method, method_params]] = method.items()
            method_params = self.convert_record(
                rules=method_params, record=self.record).convert()
            if not isinstance(method_params, list):
                method_params = [method_params]
            for method_param in method_params:
                getattr(data_class_obj, method)(**method_param)
        return asdict(data_class_obj)

    def _get_field(self, key, rec=None):
        record = rec or self.record
        if key:
            # key elemenets in nested keys are surround with "". For exmample
            # key.example-1 becomes "key"."example-1".
            # Needed for jmespath can hande special characters in the keys
            nested_keys = key.split('.')
            nested_key = '.'.join(['"' + key + '"' for key in nested_keys])
            try:
                return jmespath.search(nested_key, record)
            except jmespath.exceptions.ParseError:
                pass

        return None

    def convert_record(self, record, rules):
        """
        returns a new instance of ConvertRecord class to allow
        nested conversions to happen with the same data, command and
        (date)converter classes.
        """
        return ConvertRecord(
            record=record, rules=rules,
            data_classes=self.data_classes,
            command_class=self.command_class,
            date_coverter_class=self.date_coverter_class,
            convertor_class=self.convertor_class
        )
